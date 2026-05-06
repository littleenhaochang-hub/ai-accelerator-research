# Hardware Speculative Prefill Engine (HW-SPE) 實驗報告

## 背景與瓶頸分析
傳統的 Speculative Decoding 主要針對 Autoregressive Decoding 階段（每次一個 Token）。然而，對於長文本（例如 8K 到 128K），Prefill 階段的注意力矩陣計算 (O(N^2)) 依然是一大瓶頸。

## 解決方案：HW-SPE (硬體投機預填出)
我們提出將投機推論的概念應用於 Prefill 階段。設計一個內嵌於 NPU 的極低精度 (如 INT2 或 1-bit) **Hardware Speculative Prefill Engine (HW-SPE)**，它能在幾微秒內快速產生一組低精度的 Chunk 級別注意力特徵 (Draft)。主要的 Tensor Core 只負責平行「驗證 (Verify)」這些特徵是否符合閾值。如果符合，直接採用；若不符合，再進行精確計算。

## 實驗結果
透過 Python 模擬 (`hw_spec_prefill_sim.py`) 測試 8K Context：
- **傳統 Prefill 延遲:** 409.60 ms
- **HW-SPE 延遲:** 163.84 ms (包含 Draft 與 Verify)
- **吞吐量加速比:** 2.50x

## 結論
HW-SPE 將傳統記憶體頻寬受限的 Prefill 階段，透過極低精度推測轉化為高平行度的驗證階段，成功達到 2.50x 的加速。建議將此低精度 Draft Engine 與現有 Tensor Core 平行放置於 Edge NPU 中。
