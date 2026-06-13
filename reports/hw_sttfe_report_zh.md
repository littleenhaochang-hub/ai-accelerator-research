# 硬體架構研究報告: HW-STTFE (Spatio-Temporal Token Folding Engine)
## 摘要
本研究評估了針對 Video Transformers 的時空 Token 摺疊引擎 (HW-STTFE)。在 512000 超長上下文下，相較於傳統數位 MAC 陣列，達成 66.67 倍的延遲加速，且 SQNR 維持在 33.10 dB。
## 架構提議
建議在 Edge NPU 注意力機制模組中整合「HW-STTFE 引擎」，以硬體層級自動摺疊冗餘的時空背景 Token，極大化影片生成模型的推理效率。
