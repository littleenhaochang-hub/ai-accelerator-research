# W4A4 Quantization: FlatQuant vs QJL Hardware Overhead

## 實驗背景
根據 MEMORY.md 指示，Edge 推論必須採用 W4A4 甚至更低精度的量化以解決記憶體頻寬問題。為了抹平 Activation Outliers，我們比較了 QJL (Quantized Johnson-Lindenstrauss) 與 FlatQuant (Channel-wise Affine Smoothing) 的硬體預處理開銷。

## 硬體模擬與分析
- **腳本**: `w4a4_qjl_sim.py`
- QJL 需要進行 Hadamard Transform，延遲為 384 ns。
- FlatQuant 僅需要 Channel-wise Scaling，延遲為 32 ns。
- **效率比**: FlatQuant 的預處理速度比 QJL 快 12x。

## 架構協同設計結論
Edge AI Accelerator 應全面擁抱 FlatQuant 取代 QJL/TurboQuant 的 $O(N \log N)$ 或 $O(N^2)$ 投影矩陣。建議在 NPU 中內建原生的 Channel-wise INT4 Scaling 單元，確保 $O(N)$ 的預處理開銷不影響 Prefill/Decode 的推論管線。
