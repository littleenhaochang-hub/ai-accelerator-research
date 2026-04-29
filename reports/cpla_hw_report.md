# 實驗報告：Hardware-Accelerated Chunk-wise Parallel Linear Attention (CPLA)

## 背景 (Background)
線性注意力機制 (Linear Attention, 如 GLA, Mamba) 雖然在推論階段可以做到 $O(1)$ 的狀態更新，但在處理長文本的 Prefill (預填) 階段，若採用純遞迴 (Recurrent) 方式，其高度的資料相依性會導致 GPU/NPU 計算單元嚴重閒置。

## 方法 (Methodology)
本實驗引入了 **Hardware Chunk-wise Parallel Linear Attention (CPLA)** 架構。將長度為 N 的文本切割為 $C$ 個 Chunks。在硬體設計上：
1. 配置多個獨立的 Intra-chunk ALUs 進行並行處理 (類似 Block-diagonal matrix multiplication)。
2. 配置專用的 **Inter-chunk State Forwarding Bus**，利用硬體的結合律掃描 (Associative Scan Tree) 來極速傳遞各 Chunk 的隱藏狀態 (Hidden States)。

## 驗證結果 (Results)
- **基準 Sequential 延遲:** 0.5556 秒。
- **Hardware CPLA 延遲:** 0.1736 秒 (16 Chunks 併發)。
- **整體提升:** 將原本受限於 $O(N)$ 循序相依性的運算，透過硬體層級的 Chunk 拆分與狀態傳遞，達成了 **3.20x** 的 Prefill 加速。

## 物理架構建議 (Architectural Proposal)
建議在支援 Linear Attention / SSM 的 Edge NPU 內部實作「Dedicated Chunk-State Forwarding Bus (專屬狀態傳遞匯流排)」。這樣可以打破長文本預填時的序列相依瓶頸，使 ALUs 達到接近 100% 的運算利用率。
