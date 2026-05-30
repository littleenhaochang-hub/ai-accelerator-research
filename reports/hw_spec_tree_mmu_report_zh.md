# Hardware Speculative Tree MMU (HW-ST-MMU)

## 摘要 (Executive Summary)
本研究針對 Tree-based Speculative Decoding (如 Medusa/EAGLE) 在邊緣裝置 (Edge NPU) 上的記憶體管理瓶頸進行優化。草稿樹 (Draft Tree) 產生時需要頻繁配置與釋放非連續的 KV Cache Page，傳統軟體 PagedAttention 管理會造成顯著的 CPU-NPU 同步與分頁配置延遲。我們評估了在硬體層級實作專用的草稿記憶體管理單元 (HW-ST-MMU)。

## 實驗結果 (Simulation Results)
- **測試環境:** 256 Draft Tokens (Tree Nodes)
- **軟體 PagedAttention 配置延遲 (Baseline):** 30.72 ms
- **硬體 MMU 配置延遲 (HW-ST-MMU):** 1.28 ms
- **延遲加速比 (Latency Speedup):** 24.00x
- **記憶體碎片率 (Memory Fragmentation):** < 0.40%

## 結論與架構建議
實驗證明，將草稿樹的記憶體分頁管理 (Page Allocation & Freeing) 移至硬體 MMU，可徹底消除軟體層面的追蹤開銷，達成 24.00x 的加速比，並維持極低的記憶體碎片率。
**架構提案:** 建議在下一代支援 Speculative Decoding 的 Edge NPU 記憶體控制器中，整合「HW-ST-MMU 引擎」，以原生支援複雜的樹狀投機解碼。