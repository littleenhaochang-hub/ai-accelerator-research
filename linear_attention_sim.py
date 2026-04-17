def simulate_linear_attention_hardware(seq_len=16384, head_dim=64):
    print("Simulating O(N) Linear Attention vs O(N^2) Softmax Attention Hardware Efficiency...")
    
    # 參數設定
    mac_per_sec = 20e12  # 20 TOPS
    
    # Standard O(N^2) Attention
    # QK^T: N * N * D MACs
    # Attn * V: N * N * D MACs
    standard_macs = 2 * (seq_len ** 2 * head_dim)
    standard_latency_us = (standard_macs / mac_per_sec) * 1e6
    
    # O(N) Linear Attention (e.g., using Feature Maps like Katharopoulos et al.)
    # K^T * V: D * D * N MACs
    # Q * (K^T * V): N * D * D MACs
    linear_macs = 2 * (seq_len * head_dim ** 2)
    linear_latency_us = (linear_macs / mac_per_sec) * 1e6
    
    speedup = standard_latency_us / linear_latency_us if linear_latency_us > 0 else 0
    flop_reduction = standard_macs / linear_macs
    
    print(f"Sequence Length: {seq_len}, Head Dimension: {head_dim}")
    print(f"Standard O(N^2) MACs: {standard_macs:.0f} (Latency: {standard_latency_us:.2f} us)")
    print(f"Linear O(N) MACs: {linear_macs:.0f} (Latency: {linear_latency_us:.2f} us)")
    print(f"Hardware Speedup: {speedup:.2f}x")
    
    report_content = f"""# Linear Attention Hardware Simulation Report
## 背景 (Background)
O(N) Linear Attention (如 Katharopoulos 等人提出的特徵映射方法) 透過改變矩陣乘法順序，將傳統 O(N^2) 的注意力機制降低至 O(N)，解決長文本 Memory Bound 瓶頸。

## 模擬參數 (Parameters)
- Sequence Length: {seq_len}
- Head Dimension: {head_dim}

## 模擬結果 (Results)
- 傳統 O(N^2) 延遲: {standard_latency_us:.2f} µs
- Linear O(N) 延遲: {linear_latency_us:.2f} µs
- 運算加速比: {speedup:.2f}x

## 架構建議 (Architectural Proposal)
為了高效支援 Linear Attention，Edge NPU 需針對 **$D \times D$ 維度的小矩陣乘法**進行最佳化。有別於傳統 $N \times D$ 大規模乘法，Linear Attention 會頻繁對 Head Dimension 進行累加 (KV Accumulation)。建議硬體新增一個緊鄰 SRAM 的 **KV State Accumulator Array**，專門處理這類小維度連續更新。
"""
    with open("reports/linear_attention_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/linear_attention_report.md")

if __name__ == "__main__":
    simulate_linear_attention_hardware()
