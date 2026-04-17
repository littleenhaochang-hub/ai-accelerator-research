# W4A4 Quantization: FlatQuant vs QJL Hardware Overhead Report
## 背景 (Background)
W4A4 量化是 Edge 端必備技術。為了解決 Activation Outliers，業界提出了 QJL (Quantized Johnson-Lindenstrauss) 與 FlatQuant 兩種主要平滑方法。我們在此評估其硬體預先處理開銷。

## 模擬參數 (Parameters)
- Hidden Dimension: 4096
- NPU 向量單元: 128 lanes @ 1GHz

## 模擬結果 (Results)
- QJL (Hadamard Transform) 處理延遲: 384.00 ns
- FlatQuant (Channel-wise Scaling) 處理延遲: 32.00 ns
- 硬體處理效率比: FlatQuant 比 QJL 快了 12.00x 倍

## 架構建議 (Architectural Proposal)
儘管 QJL 具備理論上的完美降維特性，其 $O(N \log N)$ 的投影轉換在 Edge 端的 Prefill 階段仍會造成不可忽視的延遲。我們證明了採用 **FlatQuant (Channel-wise Affine Smoothing)** 搭配純 INT4 Matrix Math，僅需 $O(N)$ 的 Scaling 開銷，是更適合 Edge NPU 的硬體友善設計。我們強烈建議 NPU 應內建硬體級的 Channel-wise Scaling 單元。
