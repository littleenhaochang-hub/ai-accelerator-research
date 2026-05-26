# Hardware Dynamic LoRA Routing Evaluator (HW-DLRE)
## 針對 PEFT/LoRA 動態推論計算冗餘的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
在多代理人 (Multi-Agent) 或個性化推論場景中，常動態掛載多個 LoRA 模組。目前軟體實作對於每一個輸入 Token，都會無差別地計算「Base Model 分支」與「LoRA Adapter 分支」並相加。然而，並非每個 Token 的語意都需要被 Adapter 介入，造成極大的 MAC 算力與 DRAM 頻寬浪費。

### 2. 探索文獻 (Explore)
我們提出 Hardware Dynamic LoRA Routing Evaluator (HW-DLRE)。在 Base Model 的啟動值 (Activation) 進入 Tensor Core 前，硬體透過一個微小的 Inline 預測器評估其對當前 Task 的敏感度。若判定不需微調干預，硬體層級即動態繞過 (Bypass) 整個 LoRA 讀取與計算分支。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_dlre_sim.py` 進行模擬驗證：
- **Baseline LoRA Branch Latency:** 6.4062 ms
- **HW-DLRE Latency:** 1.8672 ms
- **Speedup (加速比):** 3.43x
- **MAC 運算量與頻寬縮減:** 65.0%

### 4. 結論
實作 HW-DLRE 能帶來 3.43x 的 LoRA 分支加速，極大化 NPU 資源利用率。建議將此「硬體 LoRA 動態路由評估器」整合入專為 Multi-Tenant AI 設計的 Edge NPU 架構中。
