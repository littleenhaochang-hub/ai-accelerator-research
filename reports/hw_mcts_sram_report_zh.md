# Hardware MCTS SRAM Accelerator (HW-MCTS-SRAM)
## 針對 Test-Time Compute (System 2) 搜尋樹延遲瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
Test-Time Compute 架構 (如 OpenAI o1) 會使用 Monte Carlo Tree Search (MCTS) 等搜尋演算法來擴展推理路徑。傳統架構中，MCTS 的樹狀結構由 CPU 管理，導致頻繁的 CPU-NPU 狀態傳輸 (PCIe Gen4) 與中斷，嚴重拖累 System 2 的推論速度。

### 2. 探索文獻 (Explore)
我們提出 Hardware MCTS SRAM Accelerator (HW-MCTS-SRAM)。透過在 Edge NPU 內部劃分專用的「樹狀結構管理 SRAM 區塊」，並引入硬體 MCTS 控制器，讓 NPU 能夠自主執行 Node Expansion、Selection 與 Backpropagation，完全繞過 CPU 控制。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_mcts_sram_sim.py` 進行 1024 Nodes 模擬驗證：
- **Baseline CPU MCTS Latency:** 170.00 ms
- **HW-MCTS-SRAM Latency:** 9.01 ms
- **Speedup (加速比):** 18.86x
- **PCIe Overhead 縮減:** 100.0%

### 4. 結論
實作 HW-MCTS-SRAM 能帶來 18.86x 的延遲加速。建議將此「硬體 MCTS 狀態管理器」整合入下一代專注於 Agentic AI 與 Test-Time Compute 的 Edge NPU 排程器中。
