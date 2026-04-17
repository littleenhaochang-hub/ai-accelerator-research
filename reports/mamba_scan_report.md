# Auto-Researcher 報告: Mamba/SSM 硬體平行掃描架構 (Parallel Scan)

## 摘要
Mamba 與其他狀態空間模型 (State Space Models, SSM) 在推論時能夠達到 $O(1)$ 的解碼時間，但在 Prefill (訓練/長文本理解) 階段，若採用傳統的 RNN 循序計算，將導致極度嚴重的延遲。本實驗探討在 Edge NPU 內建「硬體級聯綴前綴和 (Parallel Prefix Sum / Associative Scan) 樹狀運算元」，以突破 SSM 序列計算的物理瓶頸。

## 實驗設定
- 序列長度 (Seq Len): 8192 tokens
- 隱藏狀態維度 (State Dim): 128
- ALU 單步延遲: 1.0 ns

## 模擬結果
* **Baseline (Sequential Scan):** 8192.00 ns
* **Proposed (Hardware Parallel Tree):** 26.00 ns
* **硬體延遲加速比 (Speedup):** 315.08x

## 結論與架構建議
針對 Mamba/Jamba 架構的模型，傳統的 GPU/NPU 矩陣乘法單元 (MAC Arrays) 利用率極低。我們強烈建議未來的 Edge 加速器架構中整合專用的 **Associative Scan ALU Tree**。透過 $O(\log N)$ 的二元樹硬體結構平行處理前向與後向 Sweep，能將 8K 上下文的狀態更新延遲從微秒級壓縮至奈秒級，真正實現軟硬體協同最佳化 (Hardware-Software Co-Design)。
