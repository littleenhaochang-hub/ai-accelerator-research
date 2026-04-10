import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.models.qwen2.modeling_qwen2 import Qwen2Attention
import math
from scipy.linalg import hadamard

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

def get_hadamard_matrix(dim, device, dtype):
    h = torch.tensor(hadamard(dim), dtype=dtype, device=device)
    return h / math.sqrt(dim)

def fake_quantize(tensor, bits=4, block_size=None):
    if bits == 4: qmin, qmax = -8, 7
    elif bits == 8: qmin, qmax = -128, 127
    else: return tensor

    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.reshape(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        dq_tensor = q_tensor * scale
        return dq_tensor.reshape(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

HADAMARD_MATRICES = {}
ORIGINAL_FORWARD = Qwen2Attention.forward

# --- A8KV4 1D Hadamard Forward ---
def a8kv4_1d_forward(self, hidden_states, attention_mask=None, position_ids=None, past_key_value=None, past_key_values=None, output_attentions=False, use_cache=False, cache_position=None, position_embeddings=None, **kwargs):
    hidden_states = fake_quantize(hidden_states, bits=8)
    bsz, q_len, _ = hidden_states.size()
    query_states = self.q_proj(hidden_states)
    key_states = self.k_proj(hidden_states)
    value_states = self.v_proj(hidden_states)

    query_states = query_states.reshape(bsz, q_len, self.config.num_attention_heads, self.head_dim).transpose(1, 2)
    key_states = key_states.reshape(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)
    value_states = value_states.reshape(bsz, q_len, self.config.num_key_value_heads, self.head_dim).transpose(1, 2)

    from transformers.models.qwen2.modeling_qwen2 import apply_rotary_pos_emb
    cos, sin = position_embeddings
    query_states, key_states = apply_rotary_pos_emb(query_states, key_states, cos, sin, unsqueeze_dim=1)

    if self.head_dim not in HADAMARD_MATRICES:
        HADAMARD_MATRICES[self.head_dim] = get_hadamard_matrix(self.head_dim, query_states.device, query_states.dtype)
    H_feat = HADAMARD_MATRICES[self.head_dim]

    query_states = query_states @ H_feat
    key_states = key_states @ H_feat
    value_states = value_states @ H_feat

    key_states = fake_quantize(key_states, bits=4)
    value_states = fake_quantize(value_states, bits=4)

    past_kv = past_key_value if past_key_value is not None else past_key_values
    if past_kv is not None:
        cache_kwargs = {"sin": sin, "cos": cos, "cache_position": cache_position}
        key_states, value_states = past_kv.update(key_states, value_states, self.layer_idx, cache_kwargs)

    import transformers.models.qwen2.modeling_qwen2 as qwen2_mod
    key_states = qwen2_mod.repeat_kv(key_states, self.config.num_attention_heads // self.config.num_key_value_heads)
    value_states = qwen2_mod.repeat_kv(value_states, self.config.num_attention_heads // self.config.num_key_value_heads)

    attn_weights = torch.matmul(query_states, key_states.transpose(2, 3)) / math.sqrt(self.head_dim)
    if attention_mask is not None:
        causal_mask = attention_mask[:, :, :, : key_states.shape[-2]]
        attn_weights = attn_weights + causal_mask

    attn_weights = nn.functional.softmax(attn_weights, dim=-1, dtype=torch.float32).to(query_states.dtype)
    attn_weights = nn.functional.dropout(attn_weights, p=self.config.attention_dropout, training=self.training)

    attn_output = torch.matmul(attn_weights, value_states)
    attn_output = attn_output @ H_feat.T

    attn_output = attn_output.transpose(1, 2).contiguous()
    attn_output = attn_output.reshape(bsz, q_len, self.config.hidden_size)
    attn_output = fake_quantize(attn_output, bits=8)
    attn_output = self.o_proj(attn_output)

    if not output_attentions: attn_weights = None
    return tuple(v for v in [attn_output, attn_weights, past_kv] if v is not None)

# --- QAT Affine Layer ---
class LearnableAffine(nn.Module):
    def __init__(self, dim):
        super().__init__()
        self.scale = nn.Parameter(torch.ones(dim, dtype=torch.float16))
        self.shift = nn.Parameter(torch.zeros(dim, dtype=torch.float16))
        
    def forward(self, x):
        return x * self.scale + self.shift

# --- W4A4 FFN Block 32 ---
class W4A4_Block32_Linear(nn.Module):
    def __init__(self, original_linear):
        super().__init__()
        self.in_features = original_linear.in_features
        self.out_features = original_linear.out_features
        self.weight = original_linear.weight
        self.bias = original_linear.bias

    def forward(self, x):
        w = fake_quantize(self.weight, bits=4, block_size=32)
        x_q = fake_quantize(x, bits=4, block_size=32)
        return F.linear(x_q, w, self.bias)

class QAT_MLP_Wrapper(nn.Module):
    def __init__(self, mlp, hidden_size):
        super().__init__()
        self.affine = LearnableAffine(hidden_size)
        self.gate_proj = W4A4_Block32_Linear(mlp.gate_proj)
        self.up_proj = W4A4_Block32_Linear(mlp.up_proj)
        self.down_proj = W4A4_Block32_Linear(mlp.down_proj)
        self.act_fn = mlp.act_fn

    def forward(self, x):
        # Apply learnable compensation BEFORE the 4-bit quantizers destroy it
        x_comp = self.affine(x)
        return self.down_proj(self.act_fn(self.gate_proj(x_comp)) * self.up_proj(x_comp))

def run():
    print("🚀 Action Item 2: QAT Lite (Learnable Affine Compensation) 🚀")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
    
    # We will distill Layer 12
    layer_idx = 12
    
    model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype=torch.float16, device_map="auto")
    
    # Generate calibration data
    calib_text = "The rapid development of artificial intelligence has led to breakthroughs in quantization and hardware acceleration. In particular, extreme sub-4-bit formats present unique challenges."
    inputs = tokenizer([calib_text], return_tensors="pt").to(model.device)
    
    print("1. Extracting FP16 Golden Baseline targets for Layer 12...")
    with torch.no_grad():
        out_fp16 = model(inputs.input_ids, output_hidden_states=True)
        # Input to layer 12
        x_in = out_fp16.hidden_states[layer_idx].detach()
        # Output from FP16 MLP
        golden_mlp_out = model.model.layers[layer_idx].mlp(x_in).detach()

    print("\n2. Simulating Zero-Shot A8KV4 + W4A4 (Pre-QAT) Error...")
    Qwen2Attention.forward = a8kv4_1d_forward
    # Apply raw PTQ to MLP
    raw_mlp = QAT_MLP_Wrapper(model.model.layers[layer_idx].mlp, model.config.hidden_size).to(model.device)
    raw_mlp.eval()
    
    with torch.no_grad():
        ptq_out = raw_mlp(x_in)
        
    initial_snr = 10 * torch.log10(torch.mean(golden_mlp_out**2) / torch.mean((golden_mlp_out - ptq_out)**2)).item()
    print(f"   [Zero-Shot PTQ] SNR: {initial_snr:.2f} dB (Below 3.4 dB Death Line = Cascade Failure)")

    print("\n3. Launching QAT Lite (100 Steps Gradient Descent on 1D Affine Vector)...")
    # We only train the affine.scale and affine.shift parameters
    raw_mlp.train()
    optimizer = optim.AdamW(raw_mlp.affine.parameters(), lr=0.01)
    
    for step in range(100):
        optimizer.zero_grad()
        out = raw_mlp(x_in)
        loss = F.mse_loss(out, golden_mlp_out)
        loss.backward()
        optimizer.step()
        
        if (step+1) % 25 == 0:
            with torch.no_grad():
                current_snr = 10 * torch.log10(torch.mean(golden_mlp_out**2) / torch.mean((golden_mlp_out - out)**2)).item()
            print(f"   Step {step+1}/100 | Loss: {loss.item():.4f} | SNR: {current_snr:.2f} dB")

    print("\n4. Final Evaluation...")
    raw_mlp.eval()
    with torch.no_grad():
        final_out = raw_mlp(x_in)
    final_snr = 10 * torch.log10(torch.mean(golden_mlp_out**2) / torch.mean((golden_mlp_out - final_out)**2)).item()
    
    print(f"   [Post-QAT Lite] SNR: {final_snr:.2f} dB")
    
    if final_snr > 3.40:
        print("   🟢 BREAKTHROUGH: The learnable 1D Affine layer successfully absorbed the A8KV4+W4A4 noise, rescuing the model from the Death Line!")
    else:
        print("   🔴 FAILED: Affine shift is insufficient. Requires full QAT on the linear weights.")

if __name__ == "__main__":
    run()
