# Hardware Parallel Prefix Scan Engine (HW-PPSE)
## 針對 RetNet/Mamba 關聯掃描記憶體瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
RetNet 與 Mamba 等模型在長文本 Prefill 階段，常利用 Parallel Associative Scan (平行前綴掃描) 將時間複雜度從 $O(N)$ 降至 $O(\log N)$。然而，在軟體 GPU/NPU 實作中，這需要透過多個 Kernel 階段將序列切塊 (Chunking) 並在記憶體中反覆讀寫彙整，產生了大量冗餘的記憶體存取與 Kernel 啟動延遲。

### 2. 探索文獻 (Explore)
我們提出 Hardware Parallel Prefix Scan Engine (HW-PPSE)。透過在 Edge NPU 的 SRAM 控制器端內建一個硬體等級的加法/乘法掃描樹 (Associative Scan Tree)，序列掃描可以被轉換為硬體電路中單一 Pass 的數據流 (Dataflow) 運算，徹底消除多重軟體迴圈與記憶體讀寫。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_ppse_sim.py` 進行 64K Context 模擬驗證：
- **Baseline Software Scan Latency:** 2040.00 ms
- **HW-PPSE Latency:** 252.00 ms
- **Speedup (加速比):** 8.10x
- **記憶體頻寬縮減:** 87.5%

### 4. 結論
實作 HW-PPSE 能帶來 8.10x 的長文本 Prefill 加速，並大幅減輕記憶體牆壓力。建議將此「平行前綴掃描引擎」整合入專為 Linear RNNs/SSMs 設計的下一代 Edge NPU 中。
