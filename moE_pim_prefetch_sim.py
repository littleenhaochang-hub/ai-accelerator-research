import time

def simulate_moe_bottleneck(num_experts=128, hidden_dim=4096, batch_size=1):
    print("Simulating MoE CPU-GPU memory transfer bottleneck...")
    
    # Simulate expert size in memory (e.g., 4096 * 4096 parameters per expert * 2 bytes = 32 MB)
    expert_size_mb = (hidden_dim * hidden_dim * 2) / (1024 * 1024)
    print(f"Expert Size: {expert_size_mb:.2f} MB")
    
    # Simulate standard transfer (PCIe Gen4: ~32 GB/s -> 32 MB takes ~1 ms)
    pcie_bw_gbps = 32
    standard_transfer_time_ms = (expert_size_mb / 1024) / pcie_bw_gbps * 1000
    
    # Simulate Hardware PIM / Prefetching (Overlap compute and transfer, effective bandwidth doubled)
    pim_bw_gbps = 64
    pim_transfer_time_ms = (expert_size_mb / 1024) / pim_bw_gbps * 1000
    
    print(f"Standard PCIe Gen4 Transfer Time per Expert: {standard_transfer_time_ms:.4f} ms")
    print(f"Proposed PIM/Prefetch Transfer Time per Expert: {pim_transfer_time_ms:.4f} ms")
    print(f"Speedup: {standard_transfer_time_ms / pim_transfer_time_ms:.2f}x")
    
    # Simulate Routing
    print("\nRunning routing simulation...")
    active_experts = 4
    total_standard_time = standard_transfer_time_ms * active_experts
    total_pim_time = pim_transfer_time_ms * active_experts
    
    print(f"Total time for {active_experts} active experts (Standard): {total_standard_time:.4f} ms")
    print(f"Total time for {active_experts} active experts (PIM/Prefetch): {total_pim_time:.4f} ms")
    
    # Write report
    report_content = f"""# MoE PIM Prefetching Simulation Report
## 問題 (Problem)
MoE decoding 過程中的 CPU-GPU 記憶體傳輸是主要的瓶頸，因為 Experts 的參數龐大且 PCIe 頻寬有限。

## 模擬 (Simulation)
- Experts 數量: {num_experts}
- Hidden Dimension: {hidden_dim}
- 單一 Expert 大小: {expert_size_mb:.2f} MB
- PCIe Gen4 頻寬: {pcie_bw_gbps} GB/s
- 提議的 PIM 頻寬: {pim_bw_gbps} GB/s

## 結果 (Results)
- 標準傳輸時間 (每個 Expert): {standard_transfer_time_ms:.4f} ms
- PIM 傳輸時間 (每個 Expert): {pim_transfer_time_ms:.4f} ms
- 加速比: {standard_transfer_time_ms / pim_transfer_time_ms:.2f}x
"""
    with open("reports/moE_pim_prefetch_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print("Simulation complete. Report written to reports/moE_pim_prefetch_report.md")

if __name__ == "__main__":
    simulate_moe_bottleneck()
