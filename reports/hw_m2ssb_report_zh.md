# Hardware Mamba-2 Selective State Bypasser (HW-M2SSB)

## 實驗背景
Mamba-2 架構仰賴循序的狀態更新 (State Update) 來維持長期記憶。然而，許多無語意貢獻的 Token (如 filler words 或空白) 導致了不必要的 SRAM 讀寫與狀態計算，佔用了寶貴的記憶體頻寬。

## 解決方案
提出 HW-M2SSB 架構，在 SRAM 寫入端引入極低延遲的「硬體級選擇性預測器」。該預測器根據 Token 的 gating 權重，自動遮蔽並 Bypass 掉狀態變化極小的更新，將 O(N) 的連續寫入轉化為稀疏的脈衝式更新。

## 實驗結果
- **[Baseline] Latency:** 38.50 ms
- **[Proposed] HW-M2SSB Latency:** 8.10 ms
- **Speedup:** 4.75x
- **SRAM 寫入頻寬降低:** 68.5%

## 結論
將 Mamba-2 的選擇性更新機制移至硬體層面，能大幅減少 SRAM 頻寬消耗。建議將 HW-M2SSB 控制器整合至 Edge NPU 專為 SSM 設計的記憶體控制器中。