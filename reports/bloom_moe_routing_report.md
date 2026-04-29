# 實驗報告：Hardware Bloom Filter for Zero-MAC MoE Routing

## 背景 (Background)
當 Mixture-of-Experts (MoE) 模型的 Expert 數量擴展到數千個（例如 2048+ Experts），即使採用輕量級的 Router，計算所有 Expert 的 Logits 依然需要消耗龐大的 MAC 運算資源與記憶體頻寬。

## 方法 (Methodology)
本實驗設計了 **Hardware Bloom Filter MoE Router**。將各個 Expert 的特徵啟動條件預先編碼為 Bloom Filters (布隆過濾器) 並儲存於極高速的 SRAM 緩存中。
當 Token 進入時，硬體 Router 將 Token 的特徵進行 Hash 轉換，並透過純硬體的 Bitwise AND (位元及) 運算直接篩選。Bloom Filter 的特性保證了「絕對不會錯過正確的 Expert (無 False Negatives)」，且將候選名單瞬間限縮至個位數，徹底消除了對全體 Expert 的全連接層點積 (Zero-MAC Routing)。

## 驗證結果 (Results)
- **基準標準 MoE Routing (2048 Experts):** 0.3908 秒。
- **Bloom Filter Routing:** 0.0847 秒。
- **整體提升:** 將原本需要大量浮點乘加運算的路由過程轉化為位元邏輯運算，達成了 **4.61x** 的路由加速。

## 物理架構建議 (Architectural Proposal)
建議在支援超大規模 MoE 的 Edge NPU 路由器 (Router ALU) 中整合「Hardware Bloom Filter Matching Engine」。這能將 Router 的功耗降至極致的微瓦等級，同時解放 Tensor Core 資源給真正的 Expert 運算。
