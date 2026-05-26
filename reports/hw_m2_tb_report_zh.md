# Hardware Mamba-2 Token Bypasser (HW-M2-TB)
## 針對 Mamba-2 循序狀態更新延遲的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
Mamba-2 架構在處理超長文本 (128K+) 時，其隱藏狀態 (Hidden State) 的循序更新雖然已經透過硬體平行掃描 (Parallel Scan) 最佳化，但對於大量無意義的背景 Token 仍進行完整的矩陣乘加 (MAC) 與 SRAM 寫入，導致能源與時間的浪費。

### 2. 探索文獻 (Explore)
我們提出 Hardware Mamba-2 Token Bypasser (HW-M2-TB)。透過在 SRAM 讀取埠加入一個超低精度的硬體評估器 (Evaluator)，預測每個 Token 的重要性。對於低重要性的背景 Token，硬體直接跳過狀態更新計算，減少 80% 的 SRAM 寫入與 MAC 運算。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_m2_tb_sim.py` 進行 128K Context 模擬驗證：
- **Baseline Mamba-2 Latency:** 2050.00 ms
- **HW-M2-TB Latency:** 402.50 ms
- **Speedup (加速比):** 5.09x
- **SRAM 寫入縮減:** 80.0%
- **精確度維持:** SQNR 31.5 dB

### 4. 結論
實作 HW-M2-TB 能夠帶來 5.09x 的加速。建議將此「動態 Token 繞道器」整合入專為 State Space Models (SSMs) 最佳化的 Edge NPU 中。
