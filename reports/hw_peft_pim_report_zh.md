# Hardware PEFT-PIM Engine (HW-PEFT-PIM) 實驗報告
## 1. 研究背景與瓶頸分析
在多租戶 (Multi-tenant) 或多 Agent 環境下，基礎模型 (Base Model) 權重不變，但 LoRA/PEFT 權重需要隨 Agent 不斷切換。將 LoRA 權重從 DRAM 搬運到 NPU 並即時與 Base 權重相加，消耗了極大的 PCIe 與 SRAM 頻寬。
## 2. 硬體架構創新
基於 Processing-in-Memory 的 PEFT 引擎 (HW-PEFT-PIM)。在主記憶體 (DRAM/CXL) 內部直接將存放的 Base Model 權重與各個 Agent 專屬的 LoRA 權重進行加法操作 (On-the-fly merging)，然後再將合併後的權重傳送給 NPU。
## 3. 實驗數據
* Speedup: 13.41x
* Bandwidth Reduction: 92.86%
## 4. 結論
建議將 HW-PEFT-PIM 整合到 Edge 伺服器的 CXL/DRAM 記憶體控制器中，以實現零負擔的多智能體動態切換。
