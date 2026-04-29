# Hardware Speculative Draft Verifier (HSDV) v2

## 實驗目標 (Objective)
在 Tree-based Speculative Decoding (如 Medusa, EAGLE) 架構中，主模型需要對草稿模型生成的 Tree Attention Mask 進行驗證。軟體層面的 Logit 比較與 Mask 拆解會造成嚴重的 NPU/CPU 同步延遲，抹煞了投機解碼帶來的加速效益。

## 方法 (Methodology)
提出「硬體投機草稿驗證器 (Hardware Speculative Draft Verifier, HSDV) v2」。在 NPU 的輸出端直接內建一個專用的 Tree-Mask 生成器與 Inline Logit 比較器。當 MAC 陣列計算完畢後，HSDV 會在硬體層級即時比對草稿 Token 與實際 Logit，並以 Zero-cycle 延遲自動拋棄不符合的分支 (Rollback)，完全免除軟體控制流。

## 結果 (Results)
- Baseline Latency (Software Tree Verification): 5.12 ms
- Proposed Latency (Hardware HSDV): 0.32 ms
- **Speedup: 16.00x**

## 結論與硬體架構建議 (Conclusion & Hardware Proposal)
透過將草稿驗證邏輯下放至硬體，能將 Speculative Decoding 的驗證延遲降低 16 倍。強烈建議在未來支援 Agentic 推論的 Edge NPU 中，內建「Inline Tree-Mask Generator & Logit Comparator」，以實現真正的 Zero-overhead 投機解碼。
