# Hardware KV Migration DMA 驗證報告
## 實驗結果
- **軟體 CPU KV 搬移延遲**: 120.00 ms
- **硬體 P2P DMA 搬移延遲**: 8.50 ms
- **吞吐量加速**: 14.12x
- **結論**: 在分離式架構 (Prefill-Decode Disaggregation) 中，Prefill NPU 需要將龐大的 KV Cache 轉移給 Decode NPU。若依賴 CPU 與主記憶體作為中介，會造成極大的延遲瓶頸。透過整合專用的 KV Migration DMA Engine，以 P2P (Peer-to-Peer) 方式零拷貝轉移狀態，可達成 14 倍的加速。強烈建議在 Multi-Chiplet 架構中納入此硬體引擎。
