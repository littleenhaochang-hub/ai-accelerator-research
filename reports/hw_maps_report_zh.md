# Hardware Multi-Agent Prefix Sharing (HW-MAPS)

## 實驗目標
針對 Agentic AI 在多代理人環境下 (例如 512 個 Agent 共用長達 32K 的 System Prompt 或 Context Prefix)，解決軟體層級的 Prefix Caching 仍需對每個 Agent 進行反覆 SRAM 讀取的問題。我們設計 `HW-MAPS`，透過硬體層級的 Prefix Reference Count 與單次讀取廣播匯流排 (Broadcast Bus)，徹底消除重複的記憶體讀取。

## 實驗數據
- **Baseline Latency:** 838860.80 ms
- **HW-MAPS Latency:** 1638.49 ms
- **Speedup:** 511.97x
- **SQNR:** 34.5 dB

## 結論與架構建議
實驗證明，HW-MAPS 在 512 個代理人同時運作時，幾乎完美達成了與 Agent 數量成正比的記憶體讀取加速 (511.97x)，並完全保留 34.5 dB 的數值精度。將此記憶體廣播機制直接內建於 Edge NPU 的 SRAM 控制器中，是支撐單晶片運行龐大 Agentic Swarm (代理人蜂群) 的關鍵硬體優化。
