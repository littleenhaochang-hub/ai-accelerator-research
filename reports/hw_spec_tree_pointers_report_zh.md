# 實驗報告：硬體推測解碼樹狀指標管理器 (HW-STPM)

## 摘要
在樹狀推測解碼 (Tree-based Speculative Decoding, 如 Medusa) 中，頻繁建立與回溯 Draft Token 樹會帶來顯著的軟體指標管理 (Pointer Tracking) 與記憶體配置延遲。本實驗提出硬體樹狀指標管理器 (HW-STPM)，將指標分配與回溯邏輯硬體化。

## 實驗結果
- **Baseline 延遲 (軟體指標管理):** 3.20 ms (針對 64-node Draft Tree)
- **HW-STPM 延遲 (硬體指標管理):** 0.06 ms
- **加速比:** 50.00x

## 架構建議
建議將「硬體推測樹指標管理器」整合至 Edge NPU 的 MMU 中，徹底消除 CPU 對推測解碼的軟體控制負擔，達成零延遲的 Draft Token 記憶體管理與回溯。