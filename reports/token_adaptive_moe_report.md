# 自適應 Token 路由 MoE (Token-Adaptive MoE) 硬體架構報告

## 1. 實驗動機 (Motivation)
傳統的 Mixture-of-Experts (MoE) 模型中，所有 Token 都強制通過路由網路並觸發龐大的專家權重抓取 (Expert Fetching)。然而，研究顯示對於簡單字詞 (如標點符號、連接詞)，並不需要調用大型專家模型，這造成了嚴重的頻寬浪費。

## 2. 硬體-軟體協同設計提案 (Hardware-Software Co-Design)
我們提出 **「硬體級自適應 Token 路由器 (Hardware Token-Adaptive Router)」**：
*   在 NPU 內部新增一個極低精度的「複雜度預測器 (Complexity Predictor)」。
*   對於被判定為「簡單」的 Token，直接 Bypass 整個 MoE 層，改為使用預先載入 SRAM 內的微型共用 FFN (Shared Dense FFN) 進行處理。
*   只有「複雜」Token 才會觸發 DRAM 的專家權重 DMA 傳輸。

## 3. PyTorch 原型模擬結果 (Simulation Results)
透過 `token_adaptive_moe_sim.py` 的微架構模擬：
*   **基準測試 (Standard MoE)：** 所有 Token 觸發 DRAM Fetch，耗時 60.00 ms。
*   **自適應路由 (Proposed)：** 約 70% 的 Token 被 Bypass 到 SRAM FFN，平均耗時降至 18.00 ms。
*   **效能提升：** 整體吞吐量達成 **3.33x Speedup**。

## 4. 結論 (Conclusion)
自適應 Token 路由硬體能大幅削減無效的記憶體頻寬開銷，強烈建議在下一代邊緣 NPU 的網路排程器中導入此機制。
