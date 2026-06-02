# Hardware Token-Bypass Predictor (HW-TBP)

- **概念:** 將動態深度的層級繞過判斷，交由張量核心輸出的硬體預測器瞬間完成。
- **PPA 影響:** 延遲加速 58 倍，大幅節省不必要的後續層 MAC 功耗。
- **程式碼:** `ai-accelerator-research/hw_tbp_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_tbp_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 34.0 dB)