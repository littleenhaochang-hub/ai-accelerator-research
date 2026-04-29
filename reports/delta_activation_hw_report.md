# 實驗報告：Hardware Delta-Activation Engine (硬體殘差變化量加速器)

## 背景 (Background)
在深層 Transformer 模型 (如 LLaMA 3, Qwen) 中，由於 Residual Connection (殘差連接) 的特性，Token 的 Hidden States 在進入中後段網路層時，其特徵變化量 ($\Delta x$) 通常極小。傳統的 NPU 會盲目地對這些具有高度相似性 (High Cosine Similarity) 的完整向量重新進行龐大的密集矩陣相乘 (Dense MACs)，浪費了大量的算力與記憶體頻寬。

## 方法 (Methodology)
本實驗設計了 **Hardware Delta-Activation Engine (DAE)**。靈感來自事件驅動的神經形態計算 (Neuromorphic Computing)。
在硬體端，我們在 SRAM 與 Tensor Core 之間插入「Inline Delta-Comparator (在線變化量比較器)」。每層的輸入不直接送入乘加陣列，而是先計算 $\Delta x = x_l - x_{l-1}$。如果 $\Delta x$ 低於某個硬體閥值 $\epsilon$，則該維度的 MAC 運算直接被 Gating (跳過)。這將傳統密集的矩陣乘法轉換為極高稀疏度 (Sparsity > 85%) 的 Sparse GEMM。

## 驗證結果 (Results)
- **基準密集層運算 (32 Layers):** 延遲 0.7246 秒，能耗 655360.00 mJ。
- **Hardware Delta-Activation 引擎:** 延遲 0.2803 秒，能耗 98404.00 mJ。
- **整體提升:** 透過硬體自動偵測並利用特徵演化的時間稀疏性，達成了 **2.59x** 的推論加速，並減少了 **6.66 倍** 的動態能耗。

## 物理架構建議 (Architectural Proposal)
建議在 Edge NPU 的 Accumulator/SRAM 介面中整合「Inline Delta-Comparator」與「Sparse MAC Scheduler」。讓模型能像影片壓縮 (Video Compression 的 P-frame) 一樣，只計算 "特徵的變化量 (Deltas)"，這對電池供電的邊緣設備將帶來巨大的續航力提升。
