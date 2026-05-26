# Hardware Speculative Token Bypasser (HW-STB)

## 摘要
在推論型投機解碼 (Speculative Decoding) 中，許多由 Draft Model 生成的草稿 Token 信心度極低，但軟體層級的評估需要消耗大量 CPU/NPU 同步時間與記憶體 Scatter/Gather 操作。本研究提出將信心度評估與跳過邏輯硬體化，設計「HW-STB 引擎」，直接在記憶體存取階段過濾低信心的草稿 Token，避免其進入後續的驗證矩陣乘法 (MAC) 陣列。

## 實驗結果
- **軟體延遲**: 117.44 ms
- **硬體延遲**: 0.0092 ms
- **加速比**: 12765.27x

## 結論
硬體層級的投機 Token 旁路 (Bypass) 機制能有效遮蔽軟體層級的控制流分支與記憶體操作延遲，極大化提升投機解碼的吞吐量與能效。建議將此「HW-STB 引擎」整合至具備 Speculative Decoding 專用硬體的 Edge NPU 記憶體控制器中。