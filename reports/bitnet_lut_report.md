# 1.58-bit LLMs (BitNet b1.58) 與 LUT 硬體加速架構研究報告

## 研究背景與瓶頸
在先前的研究中，我們確認了長文本 Prefill 與 MoE 解碼時的記憶體頻寬瓶頸。近年 arXiv 上發布的 1.58-bit (Ternary {-1, 0, 1}) 權重量化技術 (如 BitNet b1.58)，為大幅降低記憶體頻寬與運算能耗提供了全新方向。然而，傳統 NPU / GPU 的 MAC (Multiply-Accumulate) 單元無法最大化 {-1, 0, 1} 權重的優勢。

## 原型設計 (Prototype)
我們在 `bitnet_lut_sim.py` 中建立了一個硬體與軟體協同設計 (Co-design) 的模擬：
* **Model Architecture:** 使用 BitNet b1.58 的三元權重矩陣。
* **Hardware Architecture:** 將傳統的 MAC 陣列替換為 Look-Up Table (LUT) 讀取機制。將 4 個 Ternary 權重分組 ($3^4 = 81$ 種組合)，在 Activation 進來時預先計算 81 種加法結果存入 SRAM LUT，接著將權重作為記憶體位址 (Address) 進行查表。

## 實驗結果與數據
數學分析與週期模擬顯示：
* 對於 Hidden Dimension $4096 \times 4096$ 的矩陣運算，傳統 MAC 週期約需 33.55M cycles。
* LUT 架構下，建立 LUT 需 82.9K ADD cycles，查表需 4.19M READ cycles，總計約 4.27M cycles。
* **效能提升 (Speedup):** 運算週期減少，達到 **7.84x** 理論加速。
* **能耗下降:** 由於使用 SRAM Read 與 Add 取代浮點/整數乘法，推估硬體能耗可降低 30x 以上。
* **精準度 (SQNR):** 由於 LUT 查表是數學上的等價變換，SQNR 為無損 (Infinity)，即 100% 維持原模型精度。

## 結論
1.58-bit LLM 搭配 LUT 硬體查表架構是 Edge AI (如 Mac mini 或專用 NPU) 突破 Compute-Bound 與 Memory-Bound 雙重限制的最佳解。建議下一步針對此架構進行 FPGA Verilog 原型實作，並探討 SRAM 面積 (Area) 代價的取捨。
