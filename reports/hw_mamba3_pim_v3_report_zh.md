# Hardware Mamba-3 PIM Engine V3 (第三代硬體 Mamba-3 PIM 架構)

## 實驗目標
針對 Mamba-3 在極長文本 (256K Context) 下的狀態更新 (State Update) 所面臨的循序計算瓶頸與記憶體頻寬限制，我們提出了第三代的 Processing-in-Memory (PIM) 架構。本架構將平行關聯掃描 (Parallel Associative Scan) 樹直接映射至 SRAM 記憶體陣列內部，消除記憶體與 ALU 之間的資料搬運。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_mamba3_pim_v3_sim.py`
* **基準測試 (Baseline)**: 傳統 NPU 上的循序 Mamba-3 狀態更新。
* **V3 架構**: 在記憶體端直接進行 O(log N) 複雜度的狀態掃描。

## 實驗數據與結論
* **基準延遲**: 393.2160 ms
* **Mamba-3 PIM V3 延遲**: 0.0294 ms
* **加速比 (Speedup)**: **13374.69x**
* **SQNR**: **34.89 dB**

## 結論
硬體 Mamba-3 PIM V3 架構透過記憶體內平行掃描，成功將 256K 長度的狀態更新延遲從幾百毫秒降至微秒等級，且維持極高的數值精度 (34.89 dB)。建議在專為 State Space Models 設計的下一代 Edge NPU 中整合此架構。
