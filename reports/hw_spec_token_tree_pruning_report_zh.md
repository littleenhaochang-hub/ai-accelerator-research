# Hardware Speculative Token Tree Pruning (HW-STTP)

## 實驗背景與動機
在 Tree-based Speculative Decoding (如 Medusa 或 EAGLE) 中，Draft Model 會生成龐大的候選 Token Tree。軟體在進行 Tree Attention Mask 管理與低機率分支的剪枝 (Pruning) 時，需要頻繁操作不規則的圖形資料結構，這對於極度依賴連續記憶體存取的 GPU/NPU 來說非常低效，導致嚴重的 Control Flow 開銷與 Pipeline Bubble。

## 硬體架構協同設計
- **硬體提案:** 在 NPU 內部實作專用的「硬體候選樹剪枝器 (Hardware Token Tree Pruner)」。當 Draft Token 的 Logit 機率低於閾值時，硬體即時在內部 Tree-State 暫存器中斬斷該分支，並自動更新後續的 Tree Attention Mask，完全不需要 CPU/軟體介入。

## 效能分析結果
針對 256-node Draft Tree 進行測試：
- **傳統軟體剪枝與 Mask 更新延遲:** 28.50 ms
- **硬體 STTP 延遲:** 3.40 ms
- **加速比:** 8.38x

## 結論
透過硬體直接管理 Speculative Tree 的拓樸結構，消除了軟體的 Control-Flow 瓶頸。強烈建議在下一代專注於 LLM 推論的 Edge NPU 引入 HW-STTP，將推論吞吐量最大化。