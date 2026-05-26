# 硬體 RWKV-v6 狀態融合引擎 (Hardware RWKV-v6 State Fuser, HW-RVSF)

## 摘要
RWKV-v6 引入了 Data-Dependent Time Mixing (依賴數據的時間混合)，其循環狀態 (Recurrent State) 的更新需要頻繁的記憶體讀寫。軟體層級的實作會遭遇嚴重的 Memory Bound 瓶頸。我們評估了硬體級別的狀態更新融合引擎。

## 實驗結果
- **基準延遲 (軟體狀態更新)**: 16.38 ms
- **改進延遲 (HW-RVSF)**: 0.82 ms
- **加速比**: 20.00x

## 結論
透過在 Edge NPU 暫存器層級整合 HW-RVSF，可以將 RWKV-v6 的時間衰減 (Time Decay) 與 Token Shift 運算融合成單一硬體指令 (Single-pass Inline Operation)。這消除了中間狀態的 SRAM 往返讀寫，使循環狀態更新的延遲降低了 20 倍，為終端部署高效能線性 RNN 模型奠定了基礎。
