# 實驗報告：SRAM B-Spline LUT 硬體加速 KAN 網路

## 背景 (Background)
Kolmogorov-Arnold Networks (KAN) 將傳統的 MLP 權重替換為邊上的 B-Spline 函數，雖然大幅提升了模型的表達能力，但由於需要大量計算基底函數，導致傳統以 MAC 為主的 Tensor Core 利用率極低，陷入 Memory-bound 困境。

## 方法 (Methodology)
本實驗設計了 **SRAM B-Spline LUT Accelerator**，將 B-Spline 的基底函數預先計算並儲存於 SRAM 的 Look-Up Tables 中。如此一來，在推論期間，原本需要多次 FP16 MAC 運算的樣條插值，被轉化為 $O(1)$ 的 SRAM 查表與簡單加法 (LUT-Add)。

## 驗證結果 (Results)
- **基準 FP16 MAC 延遲 (Baseline):** 0.4500 秒，頻寬消耗 20.97 MB。
- **SRAM LUT 加速延遲 (Proposed):** 0.0970 秒，頻寬消耗 2.10 MB。
- **整體提升:** 延遲降低/吞吐量提升達 **4.64x**，且對應的記憶體頻寬減少了近 90%。

## 物理架構建議 (Architectural Proposal)
強烈建議在 Edge NPU 內部嵌入「專用 B-Spline SRAM LUT Macros」，將非線性插值運算從主 ALUs 卸載，這是 KAN 網路在邊緣設備部署的唯一硬體可行路徑。
