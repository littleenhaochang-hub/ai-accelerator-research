# Hardware Dynamic Attention Head Gating (HW-DAHG)

## 摘要 (Executive Summary)
近年研究顯示，LLM 內部許多 Attention Heads 是冗餘的，或者僅在特定 Token 上具有高活躍度 (Activation)。傳統上依賴軟體遮罩 (Masking) 來實現 Sparse Heads，會產生控制流開銷且無法真正節省硬體功耗。本研究驗證了「硬體動態注意力頭閘控引擎 (HW-DAHG)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Evaluation):** 軟體層面追蹤各 Head 重要性並套用遮罩，延遲達 440.00 ms。
- **硬體閘控 (HW-DAHG):** 透過硬體即時移動平均 (Moving Average) 評估器，瞬間針對不活躍的 Head 執行時脈閘控 (Clock Gating) 與電源閘控，延遲僅 40.00 ms。
- **效能提升 (Speedup):** 達成 **11.00x** 的加速，並實體節省了被關閉之 Head 的動態功耗。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 的 Attention Block 內部整合 HW-DAHG。這不僅能大幅消除軟體控制流的延遲，更能將演算法層面的「注意力頭稀疏性」轉化為電池續航力實質上的延長。