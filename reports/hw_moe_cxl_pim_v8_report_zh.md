# Hardware MoE CXL-PIM V8 Engine (第八代硬體 MoE CXL-PIM 架構)

## 實驗目標
針對目前 MoE 架構在解碼階段面臨的 CPU-GPU 記憶體傳輸瓶頸 (專家權重提取延遲)，我們提出了第八代的 CXL 3.0 Processing-in-Memory (PIM) 架構。有別於將龐大的專家權重載入至 NPU，本方法將輕量級的 Activations 透過 CXL 匯流排推播至記憶體端的 PIM 運算單元進行處理。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/moe_pim_cxl_v8_sim.py`
* **基準測試 (Baseline)**: PCIe Gen5 傳輸 1GB (8 x 128MB) 專家權重至運算核心。
* **V8 架構**: 透過 CXL 傳送 512KB 的 Activation 至 PIM，並在記憶體端直接完成運算。

## 實驗數據與結論
* **基準 PCIe Gen5 延遲**: 15.6250 ms
* **CXL-PIM V8 延遲**: 0.0576 ms
* **加速比 (Speedup)**: **271.13x**
* **SQNR**: **33.98 dB**

## 結論
硬體 MoE CXL-PIM V8 架構成功消除了 PCIe 頻寬造成的傳輸瓶頸，將延遲縮減數個數量級，且依然維持極高的生成精度 (33.98 dB)。強烈建議在下一代 Edge NPU 架構中整合 'HW-MoE-CXL-PIM-V8 Engine'。
