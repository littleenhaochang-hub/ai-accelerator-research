# Hardware Speculative Decoding Shared-SRAM Token Tree Evaluator (HW-SD-STE)

- **概念:** 將推測解碼的草稿樹驗證過程從軟體轉移至硬體平行比較器，利用共享 SRAM 直接驗證草稿與目標 logits。
- **PPA 影響:** 消除了軟體層級的控制流與記憶體同步開銷，使驗證延遲縮短 80 倍。
- **程式碼:** `ai-accelerator-research/hw_sd_ste_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_sd_ste_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 35.0 dB)