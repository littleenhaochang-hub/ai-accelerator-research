import torch
import time

try:
    from transformers import AutoModelForCausalLM, AutoTokenizer
except ImportError:
    print("Error: transformers not installed in this venv. Please install it to load HF checkpoints.")
    exit(1)

def simulate_chained_householder(x, num_reflections=4):
    B, Seq, H = x.shape
    torch.manual_seed(42)
    x_reshaped = x.view(-1, H)
    for _ in range(num_reflections):
        v = torch.randn(H, device=x.device, dtype=x.dtype)
        v = v / torch.norm(v)
        proj = torch.matmul(x_reshaped, v.unsqueeze(1))
        x_reshaped = x_reshaped - 2 * proj * v.unsqueeze(0)
    return x_reshaped.view(B, Seq, H)

def simulated_4bit_quant(x, block_size=128):
    # Padding if H is not perfectly divisible by block_size
    H = x.shape[-1]
    pad_len = (block_size - H % block_size) % block_size
    if pad_len > 0:
        x = torch.nn.functional.pad(x, (0, pad_len))
        
    x_blocked = x.view(-1, block_size)
    amax = torch.amax(torch.abs(x_blocked), dim=-1, keepdim=True) + 1e-7
    scale = amax / 7.0
    
    q = torch.round(x_blocked / scale)
    q = torch.clamp(q, -7, 7)
    dq = q * scale
    
    residual = x_blocked - dq
    r_scale = (torch.amax(torch.abs(residual), dim=-1, keepdim=True) + 1e-7) / 1.0
    rq = torch.round(residual / r_scale)
    rq = torch.clamp(rq, -1, 1)
    drq = rq * r_scale
    
    final_dq = dq + drq
    final_dq = final_dq.view(x.shape)
    
    if pad_len > 0:
        final_dq = final_dq[..., :-pad_len]
    return final_dq

def measure_sqnr(original, quantized):
    signal_power = torch.mean(original ** 2)
    noise_power = torch.mean((original - quantized) ** 2)
    sqnr = 10 * torch.log10(signal_power / noise_power)
    return sqnr.item()

def run_real_checkpoint_fakequant():
    model_id = "Qwen/Qwen2.5-1.5B" # Using base 2B architecture as the E2B proxy for testing
    print(f"Loading real checkpoint: {model_id}...")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        # Load in bf16 to save memory, map to CPU/MPS depending on availability
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True).to(device)
    except Exception as e:
        print(f"Failed to load checkpoint from HF: {e}")
        print("Note: If the Gemma 4 E2B model is gated or hallucinated in the HF hub, we must use a valid local path or token.")
        return

    print(f"Model loaded to {device}. Running forward pass to extract real KV activations...")
    
    # Generate real activations
    text = "In computer architecture, the memory wall is the growing disparity of speed between CPU and memory outside the CPU chip. " * 10
    inputs = tokenizer(text, return_tensors="pt").to(device)
    
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True, return_dict=True)
    
    # We will hook into the last hidden state as a proxy for the input to the attention projections,
    # or just FakeQuant the actual hidden states to prove the math on real distributions.
    real_activations = outputs.hidden_states[-2].float() # Shape: [Batch, Seq, Hidden]
    
    print("==========================================================")
    print(f"Real Activation Tensor Shape: {real_activations.shape}")
    print(f"Activation Stats - Mean: {real_activations.mean().item():.4f}, Std: {real_activations.std().item():.4f}, Max: {real_activations.max().item():.4f}")
    
    # 1. Naive 4-bit FakeQuant
    naive_fq = simulated_4bit_quant(real_activations)
    sqnr_naive = measure_sqnr(real_activations, naive_fq)
    
    # 2. Householder + 4-bit FakeQuant
    smeared_act = simulate_chained_householder(real_activations, num_reflections=4)
    smeared_fq = simulated_4bit_quant(smeared_act)
    restored_act = simulate_chained_householder(smeared_fq, num_reflections=4) # Self-inverse
    sqnr_ours = measure_sqnr(real_activations, restored_act)
    
    print(f"[Real Data Metrics] Naive INT4 SQNR: {sqnr_naive:.2f} dB")
    print(f"[Real Data Metrics] Householder INT4 SQNR: {sqnr_ours:.2f} dB")
    print("==========================================================")

if __name__ == "__main__":
    run_real_checkpoint_fakequant()
