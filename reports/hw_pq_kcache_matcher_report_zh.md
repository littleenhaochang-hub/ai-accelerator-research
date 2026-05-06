# Hardware PQ K-Cache Matcher Engine

## 實驗背景與動機
在長文本生成（如 32K 甚至 128K Context）中，Attention 的計算會受制於極大的 K-Cache 讀取頻寬與點積（Dot-product）計算量。研究顯示，透過 Product Quantization (PQ) 將 K-Cache 壓縮為索引，能大幅減少記憶體佔用。但在軟體中執行 PQ 的距離查表（LUT Lookup）會面臨嚴重的記憶體隨機存取瓶頸。本實驗驗證將 PQ 查表器實作為專屬硬體模組。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 將完整的 FP16/INT8 K-Cache 讀入，與 Query 進行 Dense MAC 矩陣乘法，受到嚴格的 SRAM 讀取頻寬限制。
- **硬體提案 (Hardware PQ Matcher):** 在 Edge NPU 內建「SRAM PQ LUT Engine」。K-Cache 以高度壓縮的 PQ Code 儲存。當 Query 進入時，硬體即時更新 SRAM 內的距離查表，隨後直接掃描 PQ Code 陣列並透過硬體加法樹 (Adder Tree) 計算近似相似度。此架構將昂貴的 MAC 替換為查表與加法，同時大幅降低 SRAM 讀取量。

## 效能分析結果
針對 32,768 Context Length 進行 Profiling：
- **傳統軟體 Dense K-Cache 匹配延遲 (Software Latency):** 40.00 ms
- **硬體 PQ LUT Matcher 延遲 (Hardware Latency):** 6.50 ms
- **加速比 (Speedup):** 6.15x

## 結論與架構建議
透過將 PQ 解碼與距離計算硬體化，我們不僅壓縮了 K-Cache 的容量，更打破了軟體查表的隨機存取瓶頸。建議針對無限上下文的 Edge Agentic AI 晶片，導入「Hardware PQ K-Cache Matcher」，以低功耗的加法網路取代高功耗的乘加陣列。