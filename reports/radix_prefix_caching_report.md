# Radix Tree Prefix Caching 硬體位址轉換分析

## 實驗背景
在多輪對話或多代理人 (Multi-Agent) 協作情境下，多個請求通常會共用一段冗長的 System Prompt。若採用 Radix Tree 架構進行 Prefix Caching，可以讓這些請求在記憶體中共享同一份 KV Cache，免去重複運算 (Prefill) 與儲存。

## 實驗方法
撰寫 `radix_prefix_caching_sim.py`，模擬 10 個平行請求共享 2048 Tokens 的系統提示詞，並各自擁有 512 Tokens 的獨立提示詞。計算在標準架構與 Prefix Caching 架構下的記憶體容量與 Prefill 運算延遲。

## 實驗數據
- **Baseline KV Cache Memory**: 419.43 MB
- **Radix Prefix KV Cache Memory**: 117.44 MB
- **Memory Capacity Reduction**: 72.00%
- **Baseline Prefill Time**: 5.37 ms
- **Radix Prefix Prefill Time**: 1.93 ms (加速 2.78 倍)

## 硬體架構結論
透過 Radix Tree 的前綴快取，記憶體佔用大幅減少了 72.00%，並且 Prefill 運算速度提升了 2.78 倍。
從硬體設計的角度來看，因為虛擬的 Token 序列在實體 SRAM/DRAM 中變成了不連續且多對一的映射 (Mapping)，軟體的位址轉換會造成嚴重的延遲。Edge NPU 的記憶體管理單元 (MMU) 必須整合 **Hardware Page Table Walker (硬體分頁表尋訪器)**，用硬體直接解析 Radix Tree，達成零延遲的 Virtual-to-Physical Token 位址轉換。
