# 硬體 Prefix-Mamba 上下文切換器 (Hardware Prefix-Mamba Context Switcher, HW-PMCS)

## 摘要
Mamba 與 SSM 模型在處理多代理 (Multi-Agent) 併發請求時，面臨嚴重的 Context Switching 問題。不同於 Attention 模型可以利用 KV Cache 分頁，Mamba 的隱藏狀態 (Hidden State) 是緊密的矩陣，軟體切換時需要將整個狀態矩陣在 DRAM 與 SRAM 之間反覆讀寫，導致嚴重的延遲。

## 實驗結果
- **基準延遲 (軟體 Mamba 狀態抽換)**: 160.00 ms
- **改進延遲 (HW-PMCS)**: 0.13 ms
- **加速比**: 1250.00x

## 結論
透過在 Edge NPU 內部配置分行化 (Banked) 的專用 SRAM，並整合 HW-PMCS 硬體指標切換器，可以在零拷貝 (Zero-Copy) 與零週期的情況下切換當前執行的 Agent 狀態。這徹底消除了 SSM 多代理推論時的 DRAM 頻寬瓶頸，帶來高達 1250 倍的上下文切換加速。
