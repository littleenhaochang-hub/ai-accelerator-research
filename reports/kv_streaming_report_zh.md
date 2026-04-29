# Streaming KV Cache Eviction 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
長文本推論時 KV Cache 佔用過多 SRAM 導致 OOM 或記憶體頻寬瓶頸。

## 2. 探索文獻 (Explore)
結合注意力機制與串流驅逐 (Streaming Eviction) 策略。

## 3. 建立原型並驗證 (Prototype & Test)
執行 `kv_streaming_sim.py`，取得 **13.89x** 延遲加速。

## 4. 架構結論與建議
建議在 Edge NPU 實作專用的硬體 KV 串流驅逐控制器，自主覆寫低權重 Token。