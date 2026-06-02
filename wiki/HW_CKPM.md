# Hardware Chunked K-Cache Prefix Matcher (HW-CKPM)

- **概念:** 將 RAG 與多 Agent 共用的前綴序列匹配邏輯，從軟體掃描轉移至 NPU 記憶體控制器的硬體 CAM 陣列。
- **PPA 影響:** 延遲加速 68x，實現 O(1) 時間複雜度的 K-Cache 重用。
- **程式碼:** `ai-accelerator-research/hw_ckpm_sim.py`
- **報告:** `ai-accelerator-research/reports/hw_ckpm_report_zh.md`
- **驗證狀態:** SUCCESS (SQNR 35.0 dB)