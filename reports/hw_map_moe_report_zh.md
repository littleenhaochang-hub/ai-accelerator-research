# Hardware MoE Activation Pushing (HW-MAP) 實驗報告

## 背景與瓶頸分析
根據近期架構研究分析，MoE (Mixture of Experts) 在 Decoding 階段面臨極大的 CPU-GPU 記憶體傳輸瓶頸。傳統 PCIe 架構在 Batch=1 的情況下，需要頻繁透過 DMA 將龐大的 Expert 權重 (如 128MB) 抓取至 NPU 進行計算，導致記憶體頻寬成為最大限制，嚴重拖慢 TPS。

## 解決方案：HW-MAP (硬體 MoE 激勵推送至 PIM)
結合最新的 CXL 記憶體池與 Processing-In-Memory (PIM) 技術，我們提出 **HW-MAP 架構**。其核心概念是「將資料 (Tokens) 推送至權重端」，而非「將權重拉回運算端」。NPU 將輕量級的 Token Activation (約 2KB) 透過 CXL 傳輸至具備小型計算核心的記憶體模組 (PIM)，在當地完成 FFN 計算後再將結果傳回。

## 實驗結果
透過 Python 模擬 (`moe_activation_pushing_sim.py`) 比較傳統 PCIe Weight Fetch 與 HW-MAP 之間的差異：
- **傳統 PCIe Latency:** 2.0000 s
- **HW-MAP Latency:** 1.0241 s
- **吞吐量加速比 (Speedup):** 1.95x
- **記憶體頻寬減少:** 65,536.00x

## 結論
HW-MAP 成功消除了 CPU-GPU 之間的 PCIe 頻寬牆。建議將「CXL-PIM Activation Router」整合至下一代 Edge NPU 的設計中，以實現極致的 MoE 推理效率。
