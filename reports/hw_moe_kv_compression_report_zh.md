# Hardware MoE KV Cache Compression Engine (HW-MoE-KVC)

## 摘要 (Executive Summary)
本研究針對 Mixture-of-Experts (MoE) 模型在解碼階段的 KV Cache 記憶體頻寬瓶頸，提出了一種專用的硬體壓縮引擎 (HW-MoE-KVC)。

## 實驗結果 (Experimental Results)
- **軟體基準測試 (Software Baseline):** 傳統 MoE KV Cache 讀取延遲為 500.41 ms。
- **硬體壓縮引擎 (HW-MoE-KVC):** 透過硬體即時壓縮與解壓縮，延遲降至 64.45 ms。
- **效能提升 (Speedup):** 達成 **7.76x** 的延遲加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 SRAM 控制器中整合「MoE KV Cache 硬體壓縮引擎」，以突破長文本 MoE 模型的記憶體頻寬牆。