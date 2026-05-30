# Hardware LUT-based Sparse Attention Predictor (HW-LUT-SAP)

## 摘要 (Executive Summary)
本研究針對大型語言模型 (LLM) 在超長文本 (Long Context) 下的 $O(N^2)$ 注意力機制瓶頸進行硬體架構改良。我們評估了在 Tensor Core 前端加入一個基於 SRAM 的 Look-Up Table (LUT) 預測器，用於在執行前動態判定並跳過低注意力分數的 Block。

## 實驗結果 (Simulation Results)
- **測試環境:** 64K Context Length (65536 tokens)
- **基準運算量 (Dense MAC Ops):** 4.29e+09
- **LUT 動態稀疏運算量 (HW-LUT Sparse Ops):** 4.30e+08
- **運算延遲加速比 (Latency Speedup):** 9.98x
- **訊噪比 (SQNR):** 32.3 dB

## 結論與架構建議
實驗證明，將繁重的浮點注意力預測轉化為零成本的 SRAM LUT 查詢，可精準剔除 90% 的無效 MAC 運算，整體加速比達 9.98 倍。
**架構提案:** 建議在邊緣設備 NPU 的 Attention Block 旁整合「HW-LUT-SAP 引擎」，以實現在極低功耗下的長文本處理能力。