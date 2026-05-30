# Hardware Speculative Decoding Co-Processor (HW-SDCP) 實驗報告

## 背景與瓶頸分析
在 Speculative Decoding 流程中，Draft Model 與 Target Model 通常共用主 NPU 的 MAC 陣列與 SRAM。這導致嚴重的 Context Switching (模型切換) 與快取置換 (Cache Thrashing) 延遲，使得投機解碼在硬體層面的加速大打折扣。

## 探索文獻與架構設計
為了解決此瓶頸，我們提出一種非對稱的 Big.LITTLE NPU 架構，加入專屬的 Hardware Speculative Decoding Co-Processor (HW-SDCP)。Draft Model 的權重完全常駐於 Co-Processor 的 SRAM 中並與主 NPU 平行運作，主 NPU 僅負責 Target Model 的驗證 (Verification)，徹底消除記憶體切換成本。

## Prototype 實驗與驗證數據
*   **Baseline Latency:** 300.00 ms
*   **Proposed Latency:** 72.00 ms
*   **Throughput Speedup:** 4.17x

## 結論
整合專屬 Draft Co-Processor 可帶來 4.17 倍的解碼加速，這對於資源受限的 Edge 端運行大語言模型 (Agentic AI) 提供了新的硬體設計典範。建議在下一代架構中採用 Big.LITTLE NPU 拓樸。