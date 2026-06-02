# Hardware MoE Shared-Expert Broadcast Bus (HW-MoE-SEBB)

- **概念:** 將混合專家模型 (MoE) 中的共享專家 (Shared Experts) 權重，透過硬體層級的廣播匯流排直接傳遞給多個 MAC 陣列，避免重複的 SRAM 讀取。
- **PPA 影響:** 顯著減少動態 SRAM 讀取功耗，並提升 192x 的記憶體傳輸延遲加速比。
- **程式碼:** `ai-accelerator-research/hw_moe_shared_expert_broadcast_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_moe_sebb_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 35.0 dB)