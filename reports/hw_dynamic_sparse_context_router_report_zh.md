# Hardware Dynamic Sparse Context Router (HW-DSCR)

## 摘要 (Executive Summary)
本研究針對超長文本 (Long Context, 如 4M tokens) 在檢索增強生成 (RAG) 任務中的 Prefill 階段瓶頸進行優化。由於 RAG 文本中僅有極少數區塊包含真正相關的資訊，我們評估了在 NPU 前端加入超低精度 (INT2/1-bit) 的硬體動態稀疏上下文路由器 (HW-DSCR)，用以快速篩選並跳過無關的上下文區塊 (Chunks)。

## 實驗結果 (Simulation Results)
- **測試環境:** 1024 Chunks (約 4M Context Length)
- **基準延遲 (Dense Attention):** 1536.00 ms
- **硬體稀疏路由延遲 (HW-DSCR):** 87.04 ms
- **延遲加速比 (Latency Speedup):** 17.65x
- **訊噪比 (SQNR):** 32.3 dB

## 結論與架構建議
實驗證明，透過硬體層級的超低精度關聯性預測，能成功跳過約 95% 的無效注意力運算，在 Prefill 階段達成 17.65 倍的加速比，且對最終生成品質影響極小 (SQNR > 32 dB)。
**架構提案:** 建議在邊緣設備專為 Agentic AI 設計的 NPU 注意力單元前整合「HW-DSCR 引擎」，實現無縫的超大文本即時讀取。