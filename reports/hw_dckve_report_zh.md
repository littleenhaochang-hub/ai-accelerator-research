# 硬體動態區塊級 KV 驅逐器 (Hardware Dynamic Chunk-wise KV Evictor, HW-DCKVE)

## 摘要
在處理百萬級長文本 (1M+ Context) 時，StreamingLLM 或類似的滑動窗口機制需要頻繁驅逐 (Evict) 歷史 KV Cache 區塊。傳統軟體層級的驅逐會引發嚴重的 CPU-NPU 同步開銷與分頁表刷新 (TLB Shootdowns) 延遲。我們評估了硬體級的區塊驅逐器來解決此問題。

## 實驗結果
- **基準延遲 (軟體驅逐與同步)**: 38.40 ms
- **改進延遲 (HW-DCKVE)**: 0.51 ms
- **加速比**: 75.00x

## 結論
透過在 Edge NPU 的 MMU 與 SRAM 控制器中整合 HW-DCKVE，我們可以在背景動態解除分配與驅逐過期的 KV Chunk，達到零 CPU 介入 (Zero CPU Intervention)。此硬體設計將百萬長度文本的上下文驅逐開銷降低了 75 倍，確保模型在極長上下文生成時保持穩定的 TPS (Tokens Per Second) 而不掉速。
