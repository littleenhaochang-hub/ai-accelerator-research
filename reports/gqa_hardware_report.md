# GQA (Grouped-Query Attention) 硬體廣播架構分析

## 實驗背景
為了降低長文本推論的 KV Cache 容量與頻寬需求，多數現代 LLM (如 LLaMA-2/3) 採用了 Grouped-Query Attention (GQA)。我們進行了 GQA 的硬體層級模擬，評估其在 Edge NPU 上的 SRAM 讀取行為與潛在瓶頸。

## 實驗方法
撰寫 `gqa_hardware_sim.py`，模擬 8K Context 下，32 個 Query Heads 與 8 個 KV Heads (Group Size = 4) 的記憶體讀取量，並與標準的 MHA (Multi-Head Attention) 比較。

## 實驗數據
- **Baseline MHA KV Memory**: 134.22 MB
- **GQA KV Memory**: 33.55 MB
- **Memory Footprint Reduction**: 75.00%
- **Effective Bandwidth Speedup**: 4.00x

## 硬體架構結論
GQA 確實能在數學上將記憶體需求降低 75%。然而，在硬體實作上，如果沒有專門的廣播機制，同一個 KV Head 會被 4 個不同的 Query Heads 重複從 SRAM 中讀取，導致實際頻寬並未減少。
為了解決這個問題，邊緣 NPU 的 SRAM 讀取埠必須整合專屬的 **Query-Group Broadcaster (查詢群組廣播器)**。它能將單次讀取的 KV 資料，在硬體層級即時複製並派發給對應的 4 組 Query ALUs，達成真正的 4 倍頻寬加速，並最大化 MAC 的利用率。
