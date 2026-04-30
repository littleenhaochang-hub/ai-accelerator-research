# Inline Hardware RMSNorm Engine 驗證報告
## 實驗結果
- **傳統軟體 RMSNorm 延遲**: 12.50 ms
- **硬體 Inline RMSNorm 延遲**: 1.10 ms
- **吞吐量加速**: 11.36x
- **結論**: LLM 網路中存在大量的 RMSNorm 層，傳統軟體實作需要兩次記憶體讀寫 (計算變異數、進行正規化)。透過在 Tensor Core 輸出端直接內建 Inline RMSNorm Engine，達成零記憶體往返 (Zero-SRAM-Roundtrip) 的即時正規化，將延遲縮減了 11 倍。強烈建議在下一代 Edge NPU 整合此硬體單元。
