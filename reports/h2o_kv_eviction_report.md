# H2O (Heavy-Hitter Oracle) KV Cache 動態驅逐硬體分析

## 實驗背景
為了進一步壓縮長文本 (Long-Context) 推論時的 KV Cache 容量，我們探討了 H2O (Heavy-Hitter Oracle) 演算法的硬體實作。H2O 利用了注意力機制的稀疏性，只保留累積注意力分數最高的重要 Tokens (Heavy Hitters) 以及最近的局部視窗 (Local Window)，並動態丟棄其餘的 KV。

## 實驗方法
撰寫 `h2o_kv_eviction_sim.py`，模擬 16K 序列長度。
- 保留策略：累積注意力分數前 20% 的 Heavy Hitters，加上最近的 256 個 Tokens。
- 計算標準讀取與 H2O 動態驅逐後的記憶體頻寬差異與硬體追蹤開銷。

## 實驗數據
- **Standard KV Reads**: 268.44 MB
- **H2O Retained Tokens**: 3,532 (占比約 21.5%)
- **H2O KV Reads**: 57.87 MB
- **Memory Bandwidth Reduction**: 78.44%
- **Score Tracking Overhead**: 32.00 KB per head

## 硬體架構結論
H2O 的動態驅逐機制能有效將記憶體頻寬需求降低約 78.44%。
要在硬體上實現此機制且不產生額外延遲，Edge NPU 必須在 SRAM 控制器旁內建 **Cumulative Score Tracker (累積注意力分數追蹤器)** 與 **Dynamic Eviction Controller (動態驅逐控制器)**。只需付出每個 Attention Head 約 32 KB 的 SRAM 容量開銷，便能讓硬體自主判斷並覆寫低分 Tokens，完全釋放軟體的記憶體管理負擔。
