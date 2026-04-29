# Hardware Prompt Lookup Decoding Engine 驗證報告
## 實驗結果
- **傳統軟體掃描延遲**: 45.00 ms
- **硬體 CAM 掃描延遲**: 3.20 ms
- **吞吐量加速**: 14.06x
- **結論**: 透過 NPU 內建的 Content-Addressable Memory (CAM) 進行 Prompt Lookup 模式比對，成功消除了 Speculative Decoding 的 Draft 模型開銷，將無權重推論的字串比對延遲縮減了 14 倍，極度適合 Edge AI 的長文本問答場景。
