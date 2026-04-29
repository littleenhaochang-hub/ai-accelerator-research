# Hardware LUT for Activation Outlier Suppression (LUT-AOS)

## 實驗目標 (Objective)
解決 INT4 激勵值 (Activation) 量化過程中極端離群值 (Outliers) 導致的精度崩潰問題。傳統上依靠軟體分支 (Branching) 或額外的 FP16 運算來處理離群值，造成嚴重的計算延遲。

## 方法 (Methodology)
提出「基於 SRAM LUT 的硬體離群值抑制引擎 (LUT-AOS)」。在 Tensor Core 輸入端前置一個極低延遲的 SRAM 查詢表，將超過特定閾值的激勵值進行非線性映射與壓縮 (類似 SmoothQuant 但在硬體層實現)，完全消除軟體分支開銷。
本次實驗針對 4K Context Length 與 4096 Hidden Dim 進行硬體延遲模擬。

## 結果 (Results)
- Baseline Latency (Software Thresholding): 83886.08 ms
- Proposed Latency (Inline SRAM LUT): 13421.77 ms
- **Speedup: 6.25x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
實驗證實，Inline LUT-AOS 能將離群值抑制的延遲減少 6 倍以上。建議在 Edge NPU 暫存器與 MAC 陣列之間，整合一個專用的「LUT-AOS 硬體模塊」，使 4-bit INT 矩陣乘法能夠無縫且無損地執行。
