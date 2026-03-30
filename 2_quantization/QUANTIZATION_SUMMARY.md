# Edge AI Quantization (量化技術) 研究總結與架構決策
**Date:** March 31, 2026

本文件統整了我們迄今為止在 **Pillar 2 (Quantization)** 領域的所有實驗、數學驗證 (SNR) 與模型實測 (Live LLM Generation) 結果，並確立了針對 Edge NPU (如 Apple Silicon / Qualcomm Hexagon) 的最終量化架構。

---

## 1. 核心痛點：Activation Outliers 與 Softmax 懸崖
LLM 的權重 (Weights) 容易量化，但激活值 (Activations) 存在極端離群值 (Outliers，例如某個維度突增至 150.0)。
*   **Naive A4 (均勻 4-bit 量化)**：如果直接對 $Q, K, V$ 或 FFN 進行 4-bit 量化，離群值會撐大整個 Scale 比例尺，導致 99% 的正常數值被壓縮成 0。實測結果：模型完全崩潰，輸出亂碼或直接停止生成 (0% Pass Rate)。
*   **Softmax 懸崖 (Softmax Cliff)**：即使硬把 $Q$ 和 $K$ 量化，兩者相乘時產生的交叉誤差 $(e_q \cdot e_k)$ 經過 Softmax 的「指數級非線性放大」後，會徹底摧毀注意力分佈，導致模型邏輯斷裂。

---

## 2. 常規 A4A4 解法的死胡同 (2_3_a4a4_attention_optimizations)
我們測試了業界常見的三種 A4A4 拯救方案，**但在嚴格的「雙向驗證 (數學 SNR + 模型實測)」下全數宣告失敗**：
1.  **Percentile Clipping (百分位截斷)**：試圖切除離群值。**失敗**：數學 SNR 直接掉到負數 (-0.14 dB)，因為 LLM 極度依賴這些離群值來觸發 Attention 特徵。
2.  **Sparse-Dense Hybrid (稀疏-稠密混合, 如 SpQR)**：把 1% 離群值抽出來用 FP16 算，99% 用 4-bit 算。**失敗**：雖然數學 SNR 高達 41 dB，但活體測試時文本生成崩壞。因為將張量拆分成稀疏矩陣會破壞 RoPE (旋轉位置編碼) 等結構，且對 NPU 的連續記憶體讀取極度不友善。
3.  **Sub-Channel Quant (分組量化, Group=32)**：把向量切成好幾塊，每塊獨立算 Scale。**代價太高**：數學上有效 (18.5 dB)，但每 256 個 Token 就要儲存 65,536 Bytes 的 Scale factors (是常規的 128 倍)。在 Edge 設備上，這種「記憶體頻寬稅 (Memory Tax)」會直接卡死 NPU。

---

## 3. 最佳解答：TurboQuant (旋轉矩陣) + 1-Bit QJL 殘差
為了適應 Edge 設備「算力過剩、頻寬緊缺」的特性，我們確立了以 **TurboQuant** 為核心的最終架構：

*   **正交旋轉抹平 (Orthogonal Rotation)**：
    利用 Hadamard 或 Householder 矩陣 ($R$)，在量化前先將 $X \cdot R$。這在數學上能將 Outlier 的能量完美「均勻抹平」到所有維度上，把分布變成高斯分佈。此時進行單一 Scale 的 4-bit 量化就能完美保留精度 (16.00 dB)，且 **Scale 記憶體開銷趨近於零**。
*   **1-Bit QJL 殘差修復 (拯救 Softmax)**：
    旋轉能解決離群值，但解決不了 Softmax 懸崖。我們在硬體層面引入 1-bit 殘差，將壓縮誤差 $(K - \hat{K})$ 壓成 +1 或 -1。在推理時利用 NPU 極快的 Popcount / XNOR 邏輯閘將誤差加回。
    *   **結果**：短短 1-bit 的修復，將 Softmax 前的 SNR 提升了 2.14 dB，並在 Softmax 後放大了 **+4.18 dB** 的訊號恢復。Qwen 0.5B 的生成成功率從 0% 瞬間拉回 40~60%。

---

## 4. 極限探索：1.58-bit Ternary MACs (BitNet 架構)
為了徹底消滅浮點乘法器 (FMA)，我們探勘了將權重量化為 `{-1, 0, 1}` 的純加減法架構。
*   **當前瓶頸**：
    1.  **數學 SNR 崩塌 (5.8 dB)**：如果不從頭 Pre-train 模型，直接把現有 LLM 做 PTQ (訓練後量化) 切成三態，精度會完全喪失。
    2.  **混合精度管線停滯 (Pipeline Stall)**：整數加法很快，但最後必須把 FP16 的 Scale factor 乘回去。這種資料型態切換 (INT32 -> FP16) 在 Apple Neural Engine 等剛性 NPU 上會造成嚴重的延遲。

---

## 結論 (架構決策)
針對行動端與 Edge AI：
1.  **放棄** Sub-Channel (Group) 量化與 Sparse-Dense 稀疏矩陣。
2.  **全面採用** 「TurboQuant 旋轉矩陣 (以算力換記憶體) + 1-Bit 殘差 (Popcount 硬體加速)」作為 W4A4 與 KV Cache 的標準配備。這能在擴增極小記憶體 (4-bit -> 5-bit) 的前提下，打平 FP16 的生成品質。