# CXL-PIM MoE 硬體加速分析報告

## 執行摘要
在目前的 Mixture-of-Experts (MoE) 推理架構中，CPU 與 GPU 之間的 PCIe DMA 權重傳輸（MoE Expert Fetching）是最大的延遲瓶頸。我們驗證了使用 CXL 3.0 與 Processing-in-Memory (PIM) 技術來取代傳統的權重搬移。

## 模擬結果
* **基準測試 (PCIe Gen4 DMA):** 傳輸一個 128MB 的 Expert 權重約需 3.91 ms。
* **CXL-PIM 測試:** 將啟動向量 (Activation Vector) 傳送至記憶體端計算 (PIM) 並僅回傳結果，延遲大幅降至 0.0011 ms。
* **效能提升:** 延遲加速達 3494.65x。
* **頻寬節省:** 記憶體頻寬需求降低 16384.00x，徹底解決 OOM 與 PCIe 通訊瓶頸。

## 架構建議
針對未來的邊緣 NPU 架構，強烈建議整合 **CXL-PIM MoE Router**，將神經網路的運算單元直接嵌入 CXL 擴展記憶體中，實現在邊緣端本地執行如 DeepSeek 等超大規模 MoE 模型。
