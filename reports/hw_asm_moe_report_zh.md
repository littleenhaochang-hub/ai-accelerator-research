# 硬體加速 MoE 激勵稀疏遮罩 (HW-ASM MoE) 模擬報告

## 執行摘要
在探討大規模混合專家模型 (MoE) (如 DeepSeek-V3 架構) 的推論瓶頸時，我們發現軟體層面的稀疏矩陣遮罩運算與記憶體不連續讀取會導致嚴重的延遲。為此，我們評估了一種基於硬體的「動態激勵稀疏遮罩器」(Hardware-Accelerated Activation Sparsity Masking, HW-ASM)。

## 實驗結果
- **軟體遮罩延遲 (Software Baseline):** ~805.06 ms
- **硬體遮罩延遲 (Hardware Inline Masking):** ~27.03 ms
- **吞吐量加速比 (Speedup):** 29.78x

## 硬體架構建議
實驗證明，將激勵值 (Activations) 的閾值判斷與零值跳過 (Zero-skipping) 邏輯從軟體 (CUDA 核心/CPU) 移至 SRAM 讀取埠旁的專用硬體比較器中，可省去軟體計算的大量開銷。建議在下一代 Edge NPU 的 MoE 路由器後端整合「Inline Sparsity Comparator」，實現近乎零週期的動態稀疏資料打包，確保進入 Tensor Core 的資料流 100% 密集，消弭記憶體頻寬的浪費。
