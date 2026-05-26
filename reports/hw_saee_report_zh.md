# Hardware Sparse Autoencoder Evaluator (HW-SAEE) 實驗報告

## 摘要 (Executive Summary)
Sparse Autoencoders (SAE) 被廣泛用於解析 LLM 隱藏狀態與控制神經網路行為。然而，SAE 會將維度擴展 (Expansion) 數倍，導致極高的運算開銷。本實驗評估將 SAE 的稀疏特徵啟動與閾值過濾邏輯硬體化 (HW-SAEE)。

## 實驗結果
- **Software SAE Latency**: ~0.23 ms
- **HW-SAEE Latency**: ~0.01 ms
- **Speedup**: 28.88x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，硬體層級的平行閾值過濾器可以大幅減少高維度特徵空間展開時的延遲。我們建議在 Edge NPU 內建「HW-SAEE 引擎」，原生支援可解釋性 AI (XAI) 與 SAE 的邊緣端即時特徵解析。
