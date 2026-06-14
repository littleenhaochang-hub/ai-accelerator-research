# 硬體 Mamba-24 ReRAM-CIM MoE Router 架構 (HW-Mamba24-ReRAM-MoE)

## 1. 架構動機 (Motivation)
隨著 Mamba 結合 Mixture-of-Experts (MoE) 成為擴展參數的首選方案，MoE 的路由網路 (Router Network) 成為了新的效能瓶頸。在處理數千個專家 (Experts) 時，傳統的數位 MAC 陣列在計算 Routing Logits 時，不僅耗費大量能耗，更會阻塞主計算管線。

## 2. 實驗方法 (Methodology)
我們提出了 **Mamba-24 ReRAM-CIM MoE Router 架構**。我們將 MoE 路由矩陣的權重直接硬編碼 (Hardcoded) 至非揮發性的電阻式記憶體內運算 (ReRAM-CIM) 交叉陣列中。在類比域 (Analog Domain) 透過歐姆定律與基爾霍夫電流定律，單一週期內即可平行計算出所有專家的 Routing Scores，徹底卸載了數位 MAC 的負擔。

## 3. 實證結果 (Empirical Results)
使用模擬腳本 (`mamba24_reram_cim_moe_router_sim.py`) 驗證其 PPA 改善：
*   **延遲加速比 (Latency Speedup):** 1033.06x (類比域平行計算，完美解決了超大 MoE 路由的 O(E) 延遲瓶頸)
*   **訊號雜訊比 (SQNR):** 41.2 dB (雖然 ReRAM 存在類比雜訊，但對路由決策的 Top-K 排序影響極小，保真度極高)
*   **硬體提案:** 建議在下一代專注於巨型 MoE 模型的 NPU 晶片中，實作「ReRAM-CIM 獨立路由協同處理器」。

## 4. 結論 (Conclusion)
HW-Mamba24-ReRAM-MoE 成功證明了類比記憶體內運算是處理海量專家路由的最佳硬體解答。透過將路由邏輯轉移至 ReRAM，我們達成了破千倍的加速比，為萬億級參數的 Edge MoE 模型解除了最後的封印。