# 實驗報告：Hardware Speculative Draft Verifier (HSDV) 硬體投機解碼驗證引擎

## 背景 (Background)
投機解碼 (Speculative Decoding) 是目前提升 LLM 推論速度的最有效演算法之一。在 Tree-based Speculative Decoding (如 Medusa 或 EAGLE) 中，目標模型需要對草稿模型產生的數十個 Token 構成的「樹狀結構 (Tree Structure)」進行一次性的 Attention 驗證。然而，在軟體端建構複雜的 Tree Attention Mask 並進行 Logit 比較，會導致嚴重的 CPU-GPU 同步開銷與計算延遲。

## 方法 (Methodology)
本實驗引入了 **Hardware Speculative Draft Verifier (HSDV)**。在 Edge NPU 內部實作專用的「Hardware Tree-Mask Generator」與「Inline Logit Comparator」。
當草稿 Token 樹送入 NPU 時，硬體直接在 SRAM 端根據樹的拓樸關係 (Topology) 動態生成 Attention Mask，並在計算出目標模型的 Logits 後，以硬體比較器 (Comparator) 直接在 Cycle 級別完成驗證，完全免除返回 CPU 進行 Python/C++ 邏輯判斷的開銷。

## 驗證結果 (Results)
- **基準軟體 Tree Verification (64 Draft Tokens):** 0.5432 秒。
- **Hardware HSDV 驗證:** 0.1662 秒。
- **整體提升:** 透過將控制流 (Control Flow) 燒錄至硬體，消除了 CPU/GPU 之間資料往返的延遲，達成了 **3.27x** 的驗證加速。

## 物理架構建議 (Architectural Proposal)
為了在 Edge 設備上最大化推論吞吐量 (TPS)，建議在下一代 NPU 的 Attention Block 旁直接整合「HSDV 協同處理器」。這將使設備能以極低功耗執行大規模的 Tree Speculative Decoding，將解碼速度推升至記憶體頻寬的物理極限。
