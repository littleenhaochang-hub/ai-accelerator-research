# Hardware Dynamic Min-Max Scaler (硬體動態量化縮放器)

## 實驗背景 (Background)
在極低位元量化 (如 W4A4, KV4) 中，為了抵抗 Outliers (離群值) 對精度的破壞，通常需要使用「動態量化 (Dynamic Quantization)」，亦即在每個 Token 或 Channel 執行時，即時計算該向量的 Min/Max 與 Scale/Zero-point。但在軟體層面，這需要掃描兩次記憶體：第一次找極值，第二次套用縮放。這會造成嚴重的記憶體頻寬浪費與 Pipeline 停滯。

## 物理模擬 (Physical Simulation)
透過 `minmax_scaler_hw_sim.py` 進行了 CPU/GPU 軟體動態量化與 NPU In-line 硬體縮放器的對比：
- **軟體兩次掃描延遲 (8192 elements)**: 16.38 ms
- **硬體 In-line 即時縮放延遲**: 0.82 ms
- **整體加速比**: 20.00x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 的 SRAM Write Ports (寫入埠) 整合 **「Inline Dynamic Min-Max Scaler」**。
當 Tensor Core 計算完 Activation 或準備寫入 KV Cache 時，數據在流向 SRAM 的途中，硬體暫存器會自動更新 Running Min/Max。當一個 Block 的數據流完，硬體直接算出 Scale 並在最後一個 Clock Cycle 完成量化。這實現了「零額外記憶體讀寫」的動態量化，為 Edge NPU 提供兼顧高精度與高吞吐量的極致解法。
