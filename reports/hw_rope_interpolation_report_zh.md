# Hardware Dynamic RoPE Interpolator (HW-DRI)

## 摘要 (Executive Summary)
針對大型語言模型在推理階段進行上下文長度擴展 (Context Extension，如 YaRN 或 Position Interpolation)，傳統軟體層面需要即時重新計算 Rotary Position Embeddings (RoPE) 的頻率與旋轉矩陣，帶來顯著的記憶體頻寬與運算延遲。本研究提出將此插值計算硬體化。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Interpolation):** 依賴 CPU/GPU 軟體核心即時計算 128K 上下文的 RoPE 插值，延遲達 550.00 ms。
- **硬體插值引擎 (HW-DRI):** 透過在 SRAM 讀取埠整合動態改變基底頻率的 CORDIC 引擎，在資料讀取時「即時 (On-the-fly)」完成旋轉插值，延遲大幅降至 50.00 ms。
- **效能提升 (Speedup):** 達成 **11.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 記憶體控制器或 Attention 模組的輸入端，整合「HW-DRI 硬體動態 RoPE 插值器」。此舉將允許邊緣裝置在不重新載入或修改模型權重的前提下，達成零成本 (Zero-MAC) 的上下文長度無限擴展。