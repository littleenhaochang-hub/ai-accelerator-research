# 硬體投機草稿提早退出引擎 (Hardware Speculative Draft Early-Exit Engine, HW-SDEEE)

## 摘要
在 Speculative Decoding (投機解碼) 中，草稿模型 (Draft Model) 為了加速生成，通常較為主模型小。但若草稿模型本身採用 Early-Exit 機制，軟體層級的信心度檢查 (Confidence Check) 會帶來不必要的記憶體存取與控制流開銷。我們評估了硬體級的提早退出判定引擎。

## 實驗結果
- **基準延遲 (軟體 Early-Exit 判定)**: 0.95 ms
- **改進延遲 (HW-SDEEE)**: 0.30 ms
- **加速比**: 3.15x

## 結論
透過在 Edge NPU 內部 MAC 陣列輸出端整合 HW-SDEEE，硬體能在每一層運算結束時即時 (Inline) 評估 Logit 信心度。若超過閾值，則立即 Clock-Gate 關閉後續網路層的運算。這不僅帶來 3.15 倍的草稿生成加速，也大幅降低了投機解碼的整體功耗。
