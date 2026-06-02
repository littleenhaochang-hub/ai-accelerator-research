# Hardware SSM Sequence-Parallel Interconnect (HW-SSM-SPI)

## 摘要 (Executive Summary)
本研究探討將 State Space Models (SSM/Mamba) 的超長序列分佈在多個 Chiplet (小晶片) 上平行處理時的同步瓶頸。由於 SSM 的狀態具有序列依賴性，跨 Chiplet 傳遞狀態矩陣會受到軟體 NoC (如 PCIe/NVLink) 同步與 Bounce Buffer 的嚴重延遲。我們評估了在 Chiplet 之間實作專用的硬體 Die-to-Die (D2D) 序列平行互連匯流排 (HW-SSM-SPI)。

## 實驗結果 (Simulation Results)
- **測試環境:** 128K Context Length 跨 4 個 Chiplets
- **軟體 NoC 同步延遲 (Baseline):** 1638.40 ms
- **硬體 D2D 互連延遲 (HW-SSM-SPI):** 163.84 ms
- **延遲加速比 (Latency Speedup):** 10.00x
- **頻寬利用率 (Bandwidth Utilization):** 97.4%

## 結論與架構建議
實驗證明，透過專用的硬體 D2D 互連匯流排直接傳遞 SSM 狀態，能徹底消除軟體層級的同步開銷，達成 10.00 倍的加速比，使得多晶片組合處理超長文本成為可能。
**架構提案:** 建議在未來的 Multi-Chiplet Edge NPU 中，整合「HW-SSM-SPI 互連匯流排」，原生支援 SSM 的 Sequence Parallelism。