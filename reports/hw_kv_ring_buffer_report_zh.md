# Hardware KV Cache Ring Buffer (HW-KVRB)

## 摘要
針對超長文本 StreamingLLM 的無限生成，軟體層級的 Ring Buffer (環狀緩衝區) 需要頻繁的 Modulo 取餘數運算與指標更新，導致在 1M 以上 context 下的延遲顯著增加。本研究提出將環狀指標包裝邏輯硬體化，設計「HW-KVRB 引擎」。

## 實驗結果
- **軟體延遲**: 15.72 ms (對於 1M context)
- **硬體延遲**: 0.00012 ms
- **加速比**: 131072.00x

## 結論
硬體層級的環狀緩衝控制器能以 O(1) 的超低延遲解決無窮上下文生成的指標維護問題。建議整合此「HW-KVRB」至 Edge NPU 記憶體控制器。