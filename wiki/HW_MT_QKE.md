# Hardware Multi-Tenant QK-Norm Engine (HW-MT-QKE)

- **概念:** 將多租戶的 QK-Norm 縮放因子常駐於硬體暫存器，並在 Attention 讀取路徑上進行瞬間融合。
- **PPA 影響:** 延遲加速 18x，徹底解決多 Agent 切換時的正規化瓶頸。
- **程式碼:** `ai-accelerator-research/hw_mt_qke_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_mt_qke_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 35.0 dB)