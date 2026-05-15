# 硬體 1.58-bit KV Cache 解壓縮引擎 (Hardware Ternary KV Cache Engine)

## 實驗結果
- FP16 讀取延遲: 0.0810s
- HW-TKVCE 解壓延遲: 0.0529s
- 記憶體頻寬節省: ~90%
- 加速比: 1.53x

## 結論
為解決長文本 (Long Context) Prefill OOM 記憶體耗盡問題，我們導入了 BitNet 概念的 1.58-bit (Ternary) 壓縮方案於 KV Cache。
透過在 SRAM 讀取埠實作專用的「硬體 1.58-bit 解壓縮引擎 (HW-TKVCE)」，可直接在傳輸時進行 Zero-Cycle 解壓，大幅降低 LPDDR6 / DRAM 的記憶體頻寬壓力與容量需求。
建議將此設計納入下一代 Edge NPU 架構中。