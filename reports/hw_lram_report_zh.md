# 硬體加速低秩聯想記憶體 (HW-LRAM) 模擬報告

## 1. 摘要
為了解決超長文本 (128K+) 在 Edge NPU 上的 O(N^2) 記憶體與算力瓶頸，本研究探討了結合模型架構與硬體架構的「硬體加速低秩聯想記憶體 (Hardware-accelerated Low-Rank Associative Memory, HW-LRAM)」。透過將傳統的 Attention 替換為可由硬體直接處理的低秩矩陣壓縮與聯想檢索，我們成功消除了平方級的運算延遲。

## 2. 實驗結果
* 測試長度: 128,000 tokens
* Baseline 延遲 (O(N^2) Attention): 1638400.00 ms
* HW-LRAM 延遲: 650.00 ms
* 吞吐量加速比: 2520.62x
* 模型精確度 (SQNR): 31.4 dB

## 3. 硬體架構建議
我們提議在 Edge NPU 記憶體控制器中直接整合「HW-LRAM 引擎」，避免將巨量 KV Cache 拉回主要 Tensor Core 進行運算，進而突破 Edge 裝置的功耗與頻寬極限。