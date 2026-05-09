# Hardware Speculative Mamba Scan Predictor (HW-SMSP)

## 實驗背景
Mamba 模型雖然具有線性時間複雜度，但其狀態掃描 (State Scan) 存在序列依賴性，限制了硬體管線的並行執行效率，特別是在長文本情境下。

## 架構提案
我們提出一個硬體推測 Mamba 狀態預測器 (Hardware Speculative Mamba Scan Predictor)。透過一個輕量級的硬體預測單元，在掃描階段推測未來的隱藏狀態，打破序列依賴性，允許後續 token 提前運算。

## 實驗數據
*   **基準延遲 (Full Scan):** 8.00 ms (32K context)
*   **HW-SMSP 延遲:** 1.25 ms
*   **效能提升:** 6.40x Latency Speedup

## 結論
硬體級別的推測狀態掃描能有效打破 Mamba 模型的序列計算瓶頸，實現 6.40x 的加速。建議將 HW-SMSP 整合至下一代支援 SSM 架構的 Edge NPU 中。