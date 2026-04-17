def simulate_continuous_batching(num_requests=100, batch_size=16):
    print("Simulating Continuous Batching vs Static Batching Hardware Utilization...")
    
    # Static Batching: wait for all requests in a batch to finish
    # Assume lengths are uniformly distributed between 100 and 1000 tokens
    import random
    random.seed(42)
    req_lengths = [random.randint(100, 1000) for _ in range(num_requests)]
    
    # Static Batching Simulation
    static_total_time = 0
    for i in range(0, num_requests, batch_size):
        batch = req_lengths[i:i+batch_size]
        # Time taken is determined by the longest sequence in the batch
        static_total_time += max(batch)
        
    # Continuous Batching Simulation
    # At any point, we process up to `batch_size` tokens (one from each active request)
    # Once a request finishes, a new one is slotted in immediately.
    # Total time is roughly total tokens / batch_size + some overhead
    total_tokens = sum(req_lengths)
    continuous_total_time = total_tokens / batch_size
    
    speedup = static_total_time / continuous_total_time
    
    print(f"Total Requests: {num_requests}, Max Batch Size: {batch_size}")
    print(f"Static Batching Time (bottlenecked by longest): {static_total_time:.2f} cycles")
    print(f"Continuous Batching Time (zero idle slots): {continuous_total_time:.2f} cycles")
    print(f"Throughput Speedup: {speedup:.2f}x")
    
    report_content = f"""# Continuous Batching Hardware Scheduling Report
## 背景 (Background)
傳統 Static Batching 會因為 Batch 中序列長度不一，導致提早結束的 Request 佔用硬體氣泡 (Padding Bubbles)，嚴重浪費 MAC 單元的吞吐量。Continuous Batching (如 Orca) 能在 token-level 動態抽換 Request。

## 模擬參數 (Parameters)
- Total Requests: {num_requests}
- Batch Size: {batch_size}
- Sequence Lengths: Uniform(100, 1000)

## 模擬結果 (Results)
- Static Batching 週期: {static_total_time:.2f}
- Continuous Batching 週期: {continuous_total_time:.2f}
- 系統吞吐量提升: {speedup:.2f}x

## 架構建議 (Architectural Proposal)
為了完全釋放 Continuous Batching 的效能，Edge NPU 必須配備 **Hardware Context Switcher** 與 **Fine-grained Token Scheduler**。這允許 NPU 的排程器在硬體層級 (Cycle-level) 即時將已完成的 Token Slot 替換為等待佇列中的新 Request Token，確保 MAC Array 的利用率 (Utilization) 永遠維持在接近 100%。
"""
    with open("reports/continuous_batching_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/continuous_batching_report.md")

if __name__ == "__main__":
    simulate_continuous_batching()
