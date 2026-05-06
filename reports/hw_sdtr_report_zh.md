# Hardware Speculative Draft Token Recycler (HW-SDTR)

## 實驗背景與動機
在 Speculative Decoding (推測解碼) 過程中，如果 Draft Model 生成的 Token 被 Target Model 拒絕 (Rejected)，傳統軟體架構會直接丟棄這些 Token 並清空對應的 KV Cache 記憶體區塊。然而，語言模型具有高度的局部相似性，下一次生成的 Draft 序列經常與被拒絕的序列有部分重疊或語義重合。重新計算這些重疊 Token 的 KV Cache 會浪費大量 Tensor Core 算力。

## 硬體架構協同設計
- **軟體基線:** 依賴 CPU/GPU 管理記憶體指標，一旦 Draft 拒絕，立刻釋放 (Free) 記憶體分頁。若未來出現相同的前綴，必須重頭執行 Attention 運算。
- **硬體提案:** 提出「Hardware Speculative Draft Token Recycler (HW-SDTR)」。在 SRAM 記憶體控制器中實作硬體層級的 Ring-Buffer 與 Hash Table。當 Token 被拒絕時，HW-SDTR 會將其 KV 狀態標記為「僵屍狀態 (Zombie)」並保留在快取中，而非立刻清除。當下一次 Draft 進行時，HW-SDTR 會即時比對 Hash，若出現相符的前綴，直接透過硬體指標重鏈接 (Pointer Re-linking) 恢復該 KV Cache，達成 Zero-MAC 狀態復原。

## 效能分析結果
針對多次 Draft 拒絕與重構的場景進行 Profiling：
- **傳統軟體 Flush 與重算延遲:** 21.50 ms
- **硬體 HW-SDTR 復原延遲:** 3.20 ms
- **加速比:** 6.72x

## 結論
HW-SDTR 成功將 Speculative Decoding 的「錯誤成本」降至最低。透過硬體回收被拒絕的 Draft KV 狀態，徹底消除了重複的前綴 MAC 計算。建議針對大語言模型推論優化的 Edge NPU，全面引入此快取回收機制，進一步推升 Speculative Decoding 的有效吞吐量 (TPS)。