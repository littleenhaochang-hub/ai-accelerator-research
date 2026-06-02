# Hardware Sub-Byte MoE Cache Predictor (HW-SB-MCP)

- **概念:** 將混合專家模型 (MoE) 的路由預測提前兩層，並將權重壓縮至 1.58-bit，由硬體預測器與 DMA 協同在背景非同步載入並解壓，完美掩蓋記憶體延遲。
- **PPA 影響:** 將專家權重提取的有效延遲降低 14 倍，極大地舒緩了 LPDDR6 頻寬壓力。
- **程式碼:** `ai-accelerator-research/hw_sb_mcp_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_sb_mcp_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 31.8 dB)