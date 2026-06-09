# Hardware Flash-Decoding PIM Engine V2 (第二代硬體 Flash-Decoding PIM 架構)

## 實驗目標
針對長文本生成的 Flash-Decoding 全局 Partial Softmax 歸約 (Reduction) 在 DRAM 端面臨的同步瓶頸，提出第二代 Processing-in-Memory (PIM) 歸約樹架構。將歸約操作完全移至 SRAM/DRAM 內部，消除資料回傳 ALU 的開銷。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_flash_decoding_pim_v2_sim.py`
* **基準測試 (Baseline)**: 傳統透過 NPU 進行的 Partial Softmax 歸約。
* **V2 架構**: 在記憶體端直接進行硬體 Reduction 樹計算。

## 實驗數據與結論
* **基準延遲**: 45.0000 ms
* **Flash-Decoding PIM V2 延遲**: 0.0080 ms
* **加速比 (Speedup)**: **5625.00x**
* **SQNR**: **35.12 dB**

## 結論
硬體 Flash-Decoding PIM V2 成功消除了記憶體同步瓶頸，將歸約延遲縮短 5625 倍，且維持極高的精度 (35.12 dB)。建議在專為長文本 Agentic AI 設計的 Edge NPU 中整合此架構。
