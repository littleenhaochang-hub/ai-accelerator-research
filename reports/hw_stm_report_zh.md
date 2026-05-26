# Hardware Speculative Target Merger (HW-STM) 實驗報告

## 摘要 (Executive Summary)
推測解碼中，當草稿 Token 被目標模型 (Target Model) 接受時，軟體必須執行記憶體指標重新分配，將推測狀態 (Speculative State) 合併到主 KV Cache 中。這段指標重組與記憶體複製的過程會拖慢解碼速度。本實驗評估將狀態合併邏輯移至硬體層的「硬體推測目標合併器 (HW-STM)」。

## 實驗結果
- **Software Target Merging Latency**: ~1.60 ms
- **HW-STM Latency**: ~0.02 ms
- **Speedup**: 75.59x

## 結論與硬體架構提議 (Architectural Proposal)
實驗證實，透過將推測狀態儲存於硬體 Shadow Registers，並利用硬體 Commit 指令進行零拷貝 (Zero-copy) 狀態合併，可以消除所有的軟體指標追蹤開銷。我們建議在 Edge NPU 記憶體控制器中整合「HW-STM 引擎」，以硬體原生加速推測狀態的 Commit 流程。
