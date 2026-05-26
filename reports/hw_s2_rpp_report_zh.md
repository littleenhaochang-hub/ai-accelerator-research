# Hardware System-2 Reasoning Path Pruner (HW-S2-RPP)
## 針對 Test-Time Compute (System 2) 冗餘推論路徑的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
在 Test-Time Compute (如 OpenAI o1) 的多路徑推理 (Multi-Path Reasoning) 中，系統會同時展開數百條思考鏈。傳統架構依賴 CPU 定期介入評估並修剪 (Pruning) 錯誤路徑，這不僅造成 PCIe 通訊瓶頸，也導致 NPU 浪費大量 MAC 算力在最終會被拋棄的劣質路徑上。

### 2. 探索文獻 (Explore)
我們提出 Hardware System-2 Reasoning Path Pruner (HW-S2-RPP)。透過在 NPU 輸出端整合一個輕量級的硬體價值函數評估器 (Value Function Evaluator)，能夠在每個 Token 生成時即時更新路徑分數。一旦分數低於動態閾值，硬體將直接中斷該路徑的後續推論，完全無需 CPU 介入。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_s2_rpp_sim.py` 進行 256 條路徑模擬驗證：
- **Baseline System-2 Latency:** 27174.40 ms
- **HW-S2-RPP Latency:** 7065.60 ms
- **Speedup (加速比):** 3.85x
- **MAC 運算量縮減:** 75.0%

### 4. 結論
實作 HW-S2-RPP 能夠帶來 3.85x 的延遲加速與 75% 的運算量縮減。建議將此「硬體推理路徑修剪器」整合入下一代支援 Agentic AI 的 Edge NPU 排程器中，極大化 System-2 模型的能源效率。
