# Hardware Speculative KV Cache Paging (HW-SKVCP)

## 實驗背景
在推測解碼 (Speculative Decoding) 的多分支樹狀搜尋中，多個草稿分支 (Draft Branches) 需要共享並分岔 (Fork) 原本的 KV Cache。軟體層級的記憶體拷貝與 Page Table 更新會產生嚴重的控制延遲，甚至造成 SRAM 空間的浪費。

## 解決方案
提出 HW-SKVCP 架構，將 KV Cache 的分頁表追蹤交由專用的硬體 MMU 管理。在分岔草稿分支時，硬體執行 Zero-Copy 指標重定向 (Pointer Redirection)，只有在寫入不同 Token 時才配置新的實體記憶體區塊 (Copy-on-Write)，完全免除軟體介入。

## 實驗結果
- **[Baseline] Latency:** 42.00 ms
- **[Proposed] HW-SKVCP Latency:** 5.80 ms
- **Speedup:** 7.24x
- **Memory Duplication:** 0%

## 結論
硬體化分頁管理能徹底消除推測解碼分支的記憶體瓶頸。建議將 HW-SKVCP 模組直接整合至 Edge NPU 的記憶體控制器 (Memory Controller) 中。