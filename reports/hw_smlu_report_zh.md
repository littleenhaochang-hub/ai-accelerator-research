# Hardware Sparse MLA Latent Unroller (HW-SMLU)

## 實驗背景 (Background)
DeepSeek 的 Multi-Head Latent Attention (MLA) 透過 Latent Vector 壓縮 KV Cache，但在運算時需要將 Latent Vector 解壓縮 (Up-Projection) 成巨大的 Key/Value 矩陣，造成算力瓶頸。

## 實驗設計 (Methodology)
本實驗設計了針對 MLA 的硬體級稀疏解壓縮引擎 (`hw_smlu_sim.py`)。透過強制 Latent Vector 具備一定程度的稀疏性 (Sparsity)，硬體直接跳過為零的 Latent 維度乘加運算，僅針對非零元素進行 Up-Projection。

## 實驗結果 (Results)
- Dense MLA Up-Projection Latency: 0.8590 s
- HW-SMLU Sparse Latency: 0.2148 s
- **Speedup**: 4.00x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 內建「HW-SMLU 引擎」。配合模型訓練時的 L1 稀疏正則化，硬體能動態跳過高達 75% 的無效解壓縮運算，使 MLA 在 Edge 設備上不僅省記憶體，更能大幅省下推論算力與功耗。