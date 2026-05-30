# Hardware PIM-based SSM Normalizer (HW-PIM-SSM-Norm)

## 摘要 (Executive Summary)
本研究探討將 State Space Models (SSM) 如 Mamba 在更新隱藏狀態 (Hidden States) 時所需的 Normalization 步驟，從主 NPU ALU 移至 Processing-in-Memory (PIM) 架構中進行。由於長文本下 SSM 狀態矩陣極大，頻繁地將其從 SRAM 搬移至 ALU 進行 Normalization 會造成嚴重的頻寬浪費。

## 實驗結果 (Simulation Results)
- **測試環境:** 256K Context Length (262144 tokens)
- **傳統 SRAM-to-ALU 延遲 (Baseline):** 13107.20 ms
- **硬體 PIM 內部運算延遲 (HW-PIM-SSM-Norm):** 1966.08 ms
- **延遲加速比 (Latency Speedup):** 6.67x
- **SRAM 頻寬節省:** 100%
- **訊噪比 (SQNR):** 31.9 dB

## 結論與架構建議
實驗證明，透過 PIM 直接在記憶體陣列內部執行 Normalization，能達成 100% 的 SRAM 頻寬節省與 6.67 倍的加速，SQNR 仍穩定於 31.9 dB 左右。
**架構提案:** 建議在邊緣設備 (Edge NPU) 專用的 Mamba 晶片中整合「HW-PIM-SSM-Norm」，將所有狀態更新後的 Normalization 侷限在記憶體內部完成。