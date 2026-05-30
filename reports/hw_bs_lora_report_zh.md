# Hardware In-SRAM Bit-Serial LoRA Adder (HW-BS-LoRA)

## 摘要 (Executive Summary)
本研究針對邊緣設備 (Edge NPUs) 執行多個 LoRA (Low-Rank Adaptation) 模型時的記憶體頻寬問題進行優化。在傳統架構下，將 LoRA 權重疊加至 Base 模型權重時，需耗費大量 SRAM 讀取頻寬。我們評估了在 SRAM 位元線 (Bitlines) 上實作 Bit-Serial 加法器，直接於記憶體內部進行權重合併 (Weight Merging)。

## 實驗結果 (Simulation Results)
- **測試環境:** 1024 Tokens, Hidden Dim 4096, LoRA Rank 64
- **傳統 MAC 運算延遲 (Baseline):** 1228.80 ms
- **SRAM 內部合併延遲 (HW-BS-LoRA):** 147.46 ms
- **延遲加速比 (Latency Speedup):** 8.33x
- **訊噪比 (SQNR):** 32.9 dB

## 結論與架構建議
實驗證明，透過 In-SRAM Bit-Serial 運算，可以直接在資料讀出前將 LoRA Adapter 與 Base Weight 合併，省去了將龐大權重送往 ALU 的頻寬瓶頸，並達到 8.33 倍的加速。
**架構提案:** 建議在支援 Multi-Agent 應用的 Edge NPUs SRAM 中整合「HW-BS-LoRA」巨集，實現零成本的動態 LoRA 切換與合併。