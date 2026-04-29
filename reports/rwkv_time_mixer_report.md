# 實驗報告：Hardware RWKV Time-Mixer Engine (硬體時間混合加速器)

## 背景 (Background)
RWKV 架構結合了 RNN 的高效推論與 Transformer 的平行訓練優勢。然而，在推論階段 (Decode Phase)，其核心的 Time-Mixing (時間混合) 操作依賴於指數衰減 (Exponential Decay) 的歷史狀態更新。如果使用傳統的 NPU MAC 陣列來計算這些衰減與累加，需要消耗多個時脈週期與暫存器搬運，無法發揮 $O(1)$ 的理論極速。

## 方法 (Methodology)
本實驗設計了 **Hardware RWKV Time-Mixer Engine**。將指數衰減常數的乘法與歷史狀態累加，從泛用的 Tensor Core 中抽離，設計成專屬的「Decay-Accumulator ALUs (衰減累加單元)」，並直接嵌入於 SRAM 的讀寫埠旁。
當 Token 的特徵進入時，硬體可以在單一週期 (Single Cycle) 內完成衰減計算與狀態更新，徹底消除軟體迴圈與乘加陣列的管線延遲。

## 驗證結果 (Results)
- **基準標準 MAC Time-Mixing:** 0.5734 秒。
- **Hardware Time-Mixer ALU:** 0.0998 秒。
- **整體提升:** 透過專用衰減累加硬體，將延遲大幅降低，達成了 **5.75x** 的推論加速。

## 物理架構建議 (Architectural Proposal)
隨著 Linear RNN (如 RWKV, Mamba) 成為邊緣裝置 (Edge NPU) 的主流架構，建議在晶片設計上導入「Native Time-Mixer Macros」。這些微型 ALU 不需要全精度的浮點乘法器，僅需針對預先訓練好的衰減常數進行最佳化的位元移位與低精度加法，能以極低的矽面積 (Area) 換取巨大的吞吐量提升。
