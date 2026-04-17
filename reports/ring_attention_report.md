# Ring Attention NPU Chiplet Simulation Report
## 背景 (Background)
處理無限長度上下文 (Infinite Context) 需要極大的 KV Cache。Ring Attention 透過將 KV Cache 分佈於多個裝置 (或多個 NPU Chiplets) 的 SRAM 中，並將網路傳輸與 Attention 矩陣乘法重疊 (Overlap)，來打破單一晶片的記憶體牆。

## 模擬參數 (Parameters)
- NPU Chiplets: 4
- Total Sequence Length: 32768
- Block Size: 8192
- Inter-Chiplet Bandwidth: 100 GB/s
- NPU Throughput: 10.0 TOPS

## 模擬結果 (Results)
- 單一區塊計算時間: 0.8590 ms
- 單一區塊傳輸時間: 0.0210 ms
- 循序執行總時間: 3.5199 ms
- Ring Attention 總時間: 3.4569 ms
- 效能提升比 (Speedup): 1.02x

## 架構建議 (Architectural Proposal)
為了在 Edge AI 實現百萬等級 Context Window，應採用 Multi-Chiplet 封裝。NPU 必須具備專屬的 **D2D (Die-to-Die) Ring Interconnect** 網路介面，且支援硬體層級的非同步 DMA (Async DMA) 與雙緩衝 (Double Buffering)。這確保了當 NPU 計算當前 KV 區塊時，背景網路能無縫將下一個 KV 區塊從相鄰晶片推播過來，達到 100% Compute Bound。
