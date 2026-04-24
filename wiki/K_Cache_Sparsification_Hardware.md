# K-Cache Sparsification Hardware

為解決長文本 KV Cache 的頻寬問題，我們設計了 K-Cache 稀疏化硬體。

## 架構提案：Hardware K-Cache Sparsifier
1. 在寫入階段即時過濾極小的 K 值。
2. 採用稀疏格式儲存。
3. SRAM 讀取端內建解碼器，以 zero-cycle 進行還原。

## 實測數據
`k_cache_sparsification_sim.py` 模擬顯示，此機制能將讀取延遲從 45.00 ms 縮減至 12.50 ms，達成 **3.60x 加速**，顯著減少頻寬佔用。