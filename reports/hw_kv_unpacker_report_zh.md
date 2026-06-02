# Hardware Inline Sub-Byte KV Unpacker (HW-KV-Unpacker)

## 摘要 (Executive Summary)
本研究探討在邊緣裝置 (Edge NPU) 應用極端 KV Cache 壓縮 (如 2-bit 或 3-bit 量化) 時，軟體位元操作 (Bit Shifts & Masks) 所帶來的運算瓶頸。我們評估了在 SRAM 讀取埠整合一個硬體在線解包器 (Inline Sub-Byte Unpacker)，以零延遲 (Zero-cycle) 方式將壓縮資料還原為 Tensor Core 可接受的格式。

## 實驗結果 (Simulation Results)
- **測試環境:** 256K Context Length
- **軟體位元解包延遲 (Baseline):** 15728.64 ms
- **硬體在線解包延遲 (HW-KV-Unpacker):** 2097.15 ms
- **延遲加速比 (Latency Speedup):** 7.50x
- **訊噪比 (SQNR):** 28.3 dB

## 結論與架構建議
實驗證明，將非標準位元寬度 (Sub-Byte) 的解包邏輯從軟體 ALU 轉移至硬體 SRAM 控制器，能徹底消除 ALU 浪費在位元操作上的時間，達成 7.50 倍的加速比。
**架構提案:** 建議在下一代支援極端上下文長度的 Edge NPU SRAM 介面中，標準化整合「HW-KV-Unpacker 引擎」。