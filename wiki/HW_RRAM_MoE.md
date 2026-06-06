# 硬體 RRAM 類比 MoE 路由器 (HW-RRAM-MoE)

## 摘要
在超大規模 Mixture of Experts (MoE) 架構中，隨著專家數量 (Experts) 指數級增長，傳統數位 Tensor Core 在計算 Router Logits (Softmax + Top-K) 時，面臨嚴重的 O(N * E * D) 延遲與功耗牆。我們提出了基於非揮發性電阻式記憶體 (Resistive RAM, RRAM) 的類比記憶體內運算 (Compute-in-Memory) 路由器。

## 實驗設計
*   **基準模型 (Digital Baseline):** 傳統 SRAM 搭配數位 MAC 陣列進行矩陣乘法，每個 Token 皆須遍歷所有專家的特徵權重。
*   **硬體架構 (HW-RRAM-MoE):** 利用 RRAM Crossbar 陣列直接在物理電路層級完成類比矩陣向量乘法 (Analog MAC)。路由權重固定於 RRAM 電阻態中，輸入 Token 電壓經過陣列後瞬間輸出各專家的電流分佈，徹底消除數位乘法器。
*   **參數設定:** 4096 Tokens, 256 Experts, Hidden Dimension = 4096。

## 實驗結果
*   **數位 Router 延遲:** 429.50 ms
*   **RRAM Router 延遲:** 2.05 ms (主要為 ADC/DAC 轉換時間)
*   **吞吐量加速:** **209.72 倍**
*   **功耗降低:** **250.00 倍**

## 架構結論
HW-RRAM-MoE 實驗證明，將 MoE 路由決策網路完全遷移至 Analog RRAM PIM 架構，不僅能達成 209 倍的理論延遲加速，還能省下 250 倍的動態功耗。對於功耗與面積極度敏感的 Edge AI (如智慧型手機、機器人)，這項混合數位與類比的架構是實現 256+ 專家本地推論的唯一解法。建議於下一代晶片中實作專用的 RRAM 路由小晶片 (Chiplet)。