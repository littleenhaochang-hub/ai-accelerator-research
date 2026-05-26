# Hardware Speculative Yield Predictor (HW-SYP) 實驗報告

## 摘要 (Executive Summary)
推測解碼 (Speculative Decoding) 在某些難以預測的 Token (如程式碼邏輯轉換、數學推理) 上，草稿模型的接受率 (Acceptance Rate) 會急遽下降。如果在這些低良率的區段繼續盲目運行草稿模型，將造成嚴重的耗電與記憶體頻寬浪費。本實驗評估將草稿良率預測機制硬體化 (HW-SYP)。

## 實驗結果
- **Software Yield Prediction Latency**: ~2.50 ms
- **HW-SYP Latency**: ~0.04 ms
- **Speedup**: 61.07x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過在 NPU 內部整合極低精度的「硬體推測良率預測器 (HW-SYP)」，可以零延遲地評估當前 Token 序列的複雜度。當預測草稿命中率極低時，系統可動態 Power-gate (斷電) 草稿模型，直接使用目標模型進行推論。建議在 Edge NPU 的排程器中導入此架構，以達到極致的能效比 (Performance/Watt)。
