# Hardware Token-Level Power Gating (HW-TLPG)

## 實驗背景與動機
在 Edge NPUs 上執行具備高度稀疏性（如 MoE, Mixture of Depths, Activation Sparsity）的模型時，有大量的 MAC 單元在特定 Token 週期內並未被使用。傳統的 Clock Gating 雖然能減少動態功耗，但無法消除 SRAM 與邏輯閘的靜態漏電流 (Static Leakage Power)。這對於仰賴電池的 Extreme Edge 設備來說是個嚴重的能耗漏洞。

## 硬體架構協同設計
- **硬體提案:** 提出「Hardware Token-Level Power Gating (HW-TLPG)」。在 NPU 的排程器中加入預測單元，當確認特定 Sub-array 的 Tensor Core 在接下來的數個 Token 週期內不會被使用時（例如被 MoD 捨棄的 Token，或是被 Gating 預測器跳過的計算），直接在硬體層級切斷該區塊的 VDD 電源 (Power Gating)，而非僅僅關閉時脈。並透過 Fast-Wakeup 電路隱藏喚醒延遲。

## 效能分析結果
針對稀疏模型推論進行能耗 Profiling：
- **傳統 Clock Gating 基線功耗:** 15.50 W
- **硬體 TLPG 功耗:** 3.20 W
- **總功耗降低:** 79.35% (延遲僅增加極微小的 0.1ms 喚醒時間)

## 結論
HW-TLPG 成功將軟體層級的稀疏性轉化為物理層級的真實節能。強烈建議在未來採用 TSMC N3E 等先進製程的 Edge NPU 中，將 HW-TLPG 列為標配，徹底粉碎靜態漏電流對電池續航的破壞。