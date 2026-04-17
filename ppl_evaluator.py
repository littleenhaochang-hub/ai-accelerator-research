import torch
from datasets import load_dataset
from tqdm import tqdm

def evaluate_ppl(model, tokenizer, dataset_name="wikitext", dataset_config="wikitext-2-raw-v1", split="test", sequence_length=2048):
    """
    Evaluates the Perplexity (PPL) of a causal language model on a given dataset.
    Default dataset is WikiText-2 (standard for quantization benchmarks).
    """
    print(f"Loading {dataset_name} ({dataset_config}) split '{split}' for PPL evaluation...")
    dataset = load_dataset(dataset_name, dataset_config, split=split)
    
    print("Tokenizing dataset (this may take a moment)...")
    encodings = tokenizer("\n\n".join(dataset["text"]), return_tensors="pt")
    
    max_length = sequence_length
    stride = max_length
    seq_len = encodings.input_ids.size(1)
    
    nlls = []
    prev_end_loc = 0
    
    print(f"Evaluating PPL across {seq_len // stride} chunks of size {sequence_length}...")
    for begin_loc in tqdm(range(0, seq_len, stride), desc="Evaluating PPL"):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - prev_end_loc
        input_ids = encodings.input_ids[:, begin_loc:end_loc].to(model.device)
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100

        with torch.no_grad():
            outputs = model(input_ids, labels=target_ids)
            # loss is calculated using CrossEntropyLoss which averages over valid labels
            neg_log_likelihood = outputs.loss

        nlls.append(neg_log_likelihood)
        prev_end_loc = end_loc
        if end_loc == seq_len:
            break

    ppl = torch.exp(torch.stack(nlls).mean())
    print(f"Final PPL: {ppl.item():.4f}")
    return ppl.item()

if __name__ == "__main__":
    # Smoke test for the pipeline
    import os
    from transformers import AutoModelForCausalLM, AutoTokenizer
    
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model_id = "google/gemma-3-270m"
    cache_dir = "/Users/hao/.openclaw/workspace/offload_tmp/huggingface"
    
    token = None
    env_path = "/Users/hao/.openclaw/workspace/.env"
    if os.path.exists(env_path):
        with open(env_path, "r") as f:
            for line in f:
                if line.startswith("HF_TOKEN="): 
                    token = line.split("=")[1].strip()
                    break

    print(f"Loading {model_id} for PPL Baseline Test...")
    tokenizer = AutoTokenizer.from_pretrained(model_id, token=token, cache_dir=cache_dir)
    model = AutoModelForCausalLM.from_pretrained(
        model_id, 
        torch_dtype=torch.bfloat16, 
        low_cpu_mem_usage=True, 
        token=token, 
        cache_dir=cache_dir
    ).to(device)
    
    baseline_ppl = evaluate_ppl(model, tokenizer, sequence_length=1024)
    print(f"[Baseline Verification] {model_id} WikiText-2 PPL: {baseline_ppl:.4f}")
