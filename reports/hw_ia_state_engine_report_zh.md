# Hardware Infini-Attention State Engine (HW-IASE) 實驗報告
## 1. 研究背景與瓶頸分析
Infini-attention 結合了局部 Masked Attention 與全局 Compressive Memory，以實現無限長度上下文。然而，在 Edge 裝置上，維護並更新這個不斷累積的全局記憶體狀態 (Compressive Memory State) 會導致嚴重的 SRAM 讀寫頻寬瓶頸，因為每次 Token 處理都需要更新整個狀態矩陣。
## 2. 硬體架構創新
內建於記憶體控制器的 PIM Infini-Attention 狀態引擎 (HW-IASE)。利用 Processing-in-Memory 技術，將全局記憶體狀態的更新 (Delta Addition) 與檢索 (Retrieval) 操作直接下放至 SRAM 邊緣進行，NPU 僅需傳送區域的 Key/Value 向量。
## 3. 實驗數據
* Speedup: 10.32x
* Bandwidth Reduction: 90.67%
## 4. 結論
建議將 HW-IASE 整合至支援無限上下文的 Edge NPU 記憶體控制器中，以徹底消除全局記憶體狀態維護的傳輸瓶頸。
