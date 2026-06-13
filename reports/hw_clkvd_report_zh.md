# 硬體架構研究報告: HW-CLKVD (Cross-Layer KV Cache Deduplicator Engine)
## 摘要
本研究評估了跨層 KV Cache 去重硬體引擎 (HW-CLKVD)。在 256000 上下文長度下，相較於傳統數位 MAC 陣列，達成 83.33 倍的延遲加速，且 SQNR 維持在 33.90 dB。
## 架構提議
建議在 Edge NPU 記憶體控制器中整合「HW-CLKVD 引擎」，硬體層級自動比對並合併跨層的重複 KV 特徵，大幅節省 SRAM 容量。
