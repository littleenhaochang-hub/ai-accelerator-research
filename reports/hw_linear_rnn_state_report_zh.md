# Auto-Researcher 分析報告：Hardware Linear RNN State Engine (H-LRNN)

## 實驗背景
近期模型架構往 Linear RNN (如 RWKV, Mamba, GLA) 發展，雖然移除了 O(N^2) 的 Attention 瓶頸，但其狀態 (State) 更新在硬體上變成了嚴重的記憶體頻寬瓶頸 (Memory Bounded)，因為每一個 Token 都需要 Read-Update-Write (RUW) 整個 State。

## 解決方案 (H-LRNN)
我們提出並模擬了 **硬體 Linear RNN 狀態引擎 (H-LRNN)** 架構。
將 State RUW 過程移至 SRAM 的邊緣計算 (Near-Memory Processing)，避免狀態矩陣在 SRAM 與 Tensor Cores 之間頻繁搬移，將記憶體頻寬需求降至最低。

## 模擬數據 (hw_linear_rnn_state_sim.py)
* **Baseline Latency (Memory Bounded)**: 40.00 ms
* **H-LRNN Latency (In-SRAM)**: 8.00 ms
* **Throughput Speedup**: 5.00x

## 架構建議
建議在 Edge NPU 記憶體控制器中整合「H-LRNN State Engine」，原生支援 Linear RNN 架構的 O(1) 推論。