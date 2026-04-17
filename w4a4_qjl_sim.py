def simulate_w4a4_qjl(dim=4096):
    print("Simulating W4A4 QJL (Quantized Johnson-Lindenstrauss) vs FlatQuant hardware overhead...")
    
    # FP16 Baseline: Memory footprint for weights (dim x dim)
    fp16_weight_mb = (dim * dim * 2) / (1024 * 1024)
    
    # W4A4 Baseline footprint
    w4a4_weight_mb = (dim * dim * 0.5) / (1024 * 1024)
    
    # QJL Matrix overhead (Johnson-Lindenstrauss projection)
    # Applying random projection matrix of size dim x dim (often structured, but still overhead)
    # Assume Hadamard transform for QJL (O(N log N) addition/subtraction, no MACs)
    import math
    hadamard_ops = dim * math.log2(dim)
    # Assume NPU can do 1 op per cycle per vector lane, 1GHz, 128 lanes
    qjl_transform_ns = hadamard_ops / 128
    
    # FlatQuant overhead
    # Channel-wise affine scaling (O(N) MACs)
    flatquant_ops = dim
    flatquant_ns = flatquant_ops / 128
    
    print(f"Dimension: {dim}")
    print(f"FP16 Weights: {fp16_weight_mb:.2f} MB")
    print(f"W4A4 Weights: {w4a4_weight_mb:.2f} MB")
    print(f"QJL Transform Overhead (Hadamard): {qjl_transform_ns:.2f} ns")
    print(f"FlatQuant Transform Overhead (Scaling): {flatquant_ns:.2f} ns")
    
    speedup = qjl_transform_ns / flatquant_ns
    print(f"FlatQuant is {speedup:.2f}x faster in preprocessing latency vs QJL.")
    
    report_content = f"""# W4A4 Quantization: FlatQuant vs QJL Hardware Overhead Report
## 背景 (Background)
W4A4 量化是 Edge 端必備技術。為了解決 Activation Outliers，業界提出了 QJL (Quantized Johnson-Lindenstrauss) 與 FlatQuant 兩種主要平滑方法。我們在此評估其硬體預先處理開銷。

## 模擬參數 (Parameters)
- Hidden Dimension: {dim}
- NPU 向量單元: 128 lanes @ 1GHz

## 模擬結果 (Results)
- QJL (Hadamard Transform) 處理延遲: {qjl_transform_ns:.2f} ns
- FlatQuant (Channel-wise Scaling) 處理延遲: {flatquant_ns:.2f} ns
- 硬體處理效率比: FlatQuant 比 QJL 快了 {speedup:.2f}x 倍

## 架構建議 (Architectural Proposal)
儘管 QJL 具備理論上的完美降維特性，其 $O(N \log N)$ 的投影轉換在 Edge 端的 Prefill 階段仍會造成不可忽視的延遲。我們證明了採用 **FlatQuant (Channel-wise Affine Smoothing)** 搭配純 INT4 Matrix Math，僅需 $O(N)$ 的 Scaling 開銷，是更適合 Edge NPU 的硬體友善設計。我們強烈建議 NPU 應內建硬體級的 Channel-wise Scaling 單元。
"""
    with open("reports/w4a4_quantization_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/w4a4_quantization_report.md")

if __name__ == "__main__":
    simulate_w4a4_qjl()
