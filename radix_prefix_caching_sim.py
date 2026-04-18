import numpy as np

def simulate_prefix_caching_hardware():
    print("Starting Radix Tree Prefix Caching Hardware Simulation...")
    
    # 10 concurrent requests sharing a system prompt of 2048 tokens
    num_requests = 10
    system_prompt_len = 2048
    user_prompt_len = 512
    dim = 4096
    bytes_per_token = dim * 2 * 2 # FP16 K and V
    
    # Baseline: Independent KV cache for each request
    baseline_kv_bytes = num_requests * (system_prompt_len + user_prompt_len) * bytes_per_token
    
    # Radix Tree Prefix Caching: System prompt KV cache is shared
    shared_prefix_bytes = system_prompt_len * bytes_per_token
    user_specific_bytes = num_requests * user_prompt_len * bytes_per_token
    radix_kv_bytes = shared_prefix_bytes + user_specific_bytes
    
    memory_reduction = (1 - radix_kv_bytes / baseline_kv_bytes) * 100
    
    # Prefill Compute Latency
    npu_tflops = 100
    # O(N^2) attention compute for prefill
    baseline_flops = num_requests * ((system_prompt_len + user_prompt_len)**2) * dim * 2
    baseline_prefill_ms = (baseline_flops / 1e12) / npu_tflops * 1000
    
    # With prefix caching, system prompt is already computed (0 flops). Only compute user prompt attention against prefix + itself.
    radix_flops = num_requests * (user_prompt_len**2 + 2 * system_prompt_len * user_prompt_len) * dim * 2
    radix_prefill_ms = (radix_flops / 1e12) / npu_tflops * 1000
    
    print(f"Concurrent Requests: {num_requests}, Shared Prefix: {system_prompt_len} tokens")
    print(f"Baseline KV Cache Memory: {baseline_kv_bytes / 1e6:.2f} MB")
    print(f"Radix Prefix KV Cache Memory: {radix_kv_bytes / 1e6:.2f} MB")
    print(f"Memory Capacity Reduction: {memory_reduction:.2f}%")
    print(f"Baseline Prefill Compute Time: {baseline_prefill_ms:.2f} ms")
    print(f"Radix Prefix Prefill Compute Time: {radix_prefill_ms:.2f} ms")
    print(f"Effective Prefill Speedup: {baseline_prefill_ms / radix_prefill_ms:.2f}x")
    print("Conclusion: Prefix caching enables massive multi-tenant scale by sharing KV memory and bypassing prefill compute. Hardware requires a 'Hardware Page Table Walker' inside the MMU to natively resolve Radix Tree virtual-to-physical token mappings with zero latency.")

if __name__ == "__main__":
    simulate_prefix_caching_hardware()