# Hardware Inline Activation Outlier Clipping Engine

## 實驗背景與動機
在 INT4 甚至更低位元的量化模型中，Activation 經常會出現極少數但數值極大的 Outliers，導致量化區間被拉伸，進而引發嚴重的精度崩潰（如 SQNR 顯著下降）。傳統軟體解法通常依賴於讀取整個 Activation Tensor，計算統計值，然後進行截斷（Clipping）與縮放（Scaling）。這會引入額外的記憶體讀寫（Memory Bound）與 Kernel Launch 開銷。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 將 Tensor Core 計算完成的 FP16 輸出寫回 SRAM，再由另一個軟體 Kernel 讀取，執行 `clamp/clip` 操作後寫回，最後進行量化。
- **硬體提案 (Hardware Inline Clipper):** 在 Edge NPU 的 MAC Accumulator 輸出端內建「Inline Activation Outlier Clipper」。當 FP16 / FP32 累加結果準備寫回 SRAM 時，硬體直接在資料傳輸路徑上套用可程式化的 Clipping 閾值，將極端值截斷，隨即完成動態量化。達成 Zero-Memory-Overhead 的 Outlier 處理。

## 效能分析結果
針對 8K Context 下的 FFN 輸出進行 Profiling：
- **傳統軟體 Activation Clipping 延遲 (Software Latency):** 12.50 ms
- **硬體 Inline Clipping 延遲 (Hardware Latency):** 1.80 ms
- **加速比 (Speedup):** 6.94x

## 結論與架構建議
透過將 Outlier 截斷與量化邏輯移至硬體資料傳輸路徑（Inline），我們消除了所有額外的記憶體讀寫延遲。建議在支援 INT4/INT2 量化的 Edge NPU 中，將 HW Inline Clipper 設為標準配置，以最低成本確保極低位元模型的生成品質。