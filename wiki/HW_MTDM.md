# Hardware MoE Token-Dropping Monitor (HW-MTDM)

- **概念:** 在 MoE 路由器前端加入硬體移動平均門檻監控器，動態判斷並丟棄信心度極低的 Token，避免浪費記憶體頻寬去提取無用的專家權重。
- **PPA 影響:** 延遲加速 62.5 倍，有效減少 PCIe/LPDDR 頻寬浪費。
- **程式碼:** `ai-accelerator-research/hw_mtdm_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_mtdm_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 34.5 dB)