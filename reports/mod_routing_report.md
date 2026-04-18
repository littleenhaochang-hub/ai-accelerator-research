# Mixture-of-Depths (MoD) 動態 Token 路由硬體分析

## 實驗背景
為了進一步榨出 LLM 的算力效率，我們研究了近期提出的 Mixture-of-Depths (MoD) 架構。與傳統的 Transformer 每一層都處理所有 Tokens 不同，MoD 會透過一個小型的 Router 決定哪些 Tokens 可以跳過 (Bypass) 特定的層次 (如只允許 50% 的 Tokens 參與 Attention 與 FFN)，從而達到減少整體 MAC 運算的目標。

## 實驗方法
撰寫 `mod_routing_sim.py`，模擬 32 層、Context Length 8192 的模型。設定其中一半的層級套用 MoD，並且 Capacity Factor 設為 50% (即只處理 Top-50% 權重的 Tokens)，並計算整體的運算量與能耗縮減。

## 實驗數據
- **Baseline Compute**: 8796.09 G-MACs
- **MoD Compute**: 6597.07 G-MACs
- **Compute Energy Reduction**: 25.00%

## 硬體架構結論
MoD 能夠透過層級間的 Token 選擇，穩健地降低 25.00% 的總體運算量。
然而，在硬體上實作 MoD 會面臨「記憶體碎片化 (Memory Fragmentation)」的問題，因為被挑選出來的 Tokens 在實體 SRAM 中是不連續的。為了避免 Gathering/Scattering 帶來的記憶體頻寬懲罰，Edge NPU 必須在跨層 SRAM 緩衝區實作 **Token Bypasser & Router (Token 繞道與路由邏輯)**，在硬體層面動態遮蔽 (Mask out) 不活躍的 Tokens，確保連續的資料讀取與運算管線不受干擾。
