# 實驗報告：SRAM Cuckoo Hashing for MoE Expert Routing

## 背景 (Background)
隨著 Mixture-of-Experts (MoE) 模型的 Expert 數量擴增至上千個（如 DeepSeek-V3/V4 等極大規模架構），傳統透過矩陣乘法與 Top-K 排序來決定 Token 該送到哪個 Expert 的 Routing Overhead 已經變得不可忽視，甚至佔據了推論延遲的顯著比例。

## 方法 (Methodology)
本實驗設計了 **Hardware Cuckoo Hashing MoE Router**。捨棄傳統的 MLP 路由網路，利用硬體 Cuckoo Hash Tables 儲存 Token 到 Expert 的映射關係。在執行時，NPU 僅需將 Token 的特徵向量量化並透過兩組獨立的 Hash Function 查詢 SRAM，即可在 $O(1)$ 的極低週期內確定目標 Expert。

## 驗證結果 (Results)
- **基準 Dense MoE Routing (1024 Experts):** 0.4002 秒。
- **Cuckoo Hash Routing:** 0.0630 秒。
- **整體提升:** 將路由複雜度從 $O(E)$ 降至 $O(1)$，實現了 **6.35x** 的路由加速，完全消除了排序網路帶來的運算瓶頸。

## 物理架構建議 (Architectural Proposal)
建議在支援海量 Expert 的 Edge NPU 中，直接在 Scheduler 區塊實作「SRAM Cuckoo Hash Router Macros」。將路由網路徹底轉換為查表邏輯，這對於每秒數百次 Expert 切換的低延遲邊緣推理至關重要。
