# Hardware Activation Checkpoint Compressor (HACC) 驗證報告
## 實驗結果
- **傳統密集群體 Checkpoint DRAM 延遲**: 65.00 ms
- **硬體 Inline 壓縮延遲**: 12.50 ms
- **吞吐量加速**: 5.20x
- **結論**: 在 Edge 裝置上進行 On-Device Training (如 LoRA 微調) 時，Activation Checkpointing 是節省記憶體容量的關鍵，但會引發巨大的 DRAM 讀寫頻寬瓶頸。透過在 NPU 記憶體控制器寫入端內建 HACC，利用硬體進行即時 Block-Floating-Point 壓縮與稀疏遮罩，能將 DRAM 存取延遲降低 5 倍以上。強烈建議在支援終端學習的 Edge NPU 納入此硬體單元。
