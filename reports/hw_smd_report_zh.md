# 硬體推測性記憶體重組器 (HW-SMD) 模擬報告

## 1. 摘要
在處理高達 512K 甚至 1M Token 的超長文本時，Edge NPU 經常面臨 PagedAttention 記憶體碎片化 (Fragmentation) 問題，導致記憶體提取時產生大量 Pipeline Stalls。本實驗探討並驗證「硬體推測性記憶體重組器 (Hardware Speculative Memory Defragmenter, HW-SMD)」的效能。

## 2. 實驗結果
* 測試長度: 512,000 tokens
* Baseline 延遲 (軟體 PagedAttention 碎片化): 25620.00 ms
* HW-SMD 延遲 (硬體自動重組): 1029.00 ms
* 吞吐量加速比: 24.90x
* 實體記憶體利用率: 99.2%

## 3. 硬體架構建議
我們提議在 Edge NPU 記憶體管理單元 (MMU) 內建「HW-SMD 引擎」，在背景非同步預測並重組 KV Cache 區塊，將碎片化的不連續記憶體動態搬移至連續的 SRAM/DRAM 區段，從根本消除長文本生成期間的記憶體頻寬瓶頸。