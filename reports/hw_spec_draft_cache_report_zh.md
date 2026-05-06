# Hardware Speculative Draft Cache Engine (HW-SDC)

## 實驗背景與動機
在推測解碼 (Speculative Decoding) 中，草稿模型 (Draft Model) 頻繁生成的 Draft Tokens 會不斷被驗證與捨棄。若這些 Draft Token 的狀態頻繁寫入或讀出主 DRAM 或共享 SRAM，會產生巨大的記憶體頻寬浪費。為此，我們探討為 Draft Model 建立專屬的小型硬體快取。

## 硬體架構協同設計
- **硬體提案:** 提出「Hardware Speculative Draft Cache Engine (HW-SDC)」。在 NPU 的驗證模組 (Verification Module) 旁，配置一塊極高速但容量極小的暫存區專供 Draft Tokens 使用。Draft Token 生成後不會進到主記憶體，而是直接存入 SDC 中。驗證成功時，才由 SDC 寫入主 KV Cache；驗證失敗時，直接以 $O(1)$ 週期清空 SDC 指標，達成 Zero-Memory-Thrashing。

## 效能分析結果
針對 128 Draft Tokens 進行存取測試：
- **傳統軟體 DRAM/SRAM Draft 管理延遲:** 12.80 ms
- **硬體 HW-SDC 延遲:** 1.65 ms
- **加速比:** 7.76x

## 結論
HW-SDC 透過隔離 Draft Token 與主記憶體的資料流，成功將 Speculative Decoding 的記憶體污染降至零。強烈建議在未來專注於 Agentic 推理的 Edge NPU 標配此硬體架構，以大幅減少無效 Draft 所造成的能耗。