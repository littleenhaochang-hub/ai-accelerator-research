# MoE Embedding Near-Memory Processing (NMP) 驗證報告
## 實驗結果
- **傳統 DRAM 抓取延遲**: 55.00 ms
- **NMP 近記憶體處理延遲**: 4.20 ms
- **吞吐量加速**: 13.10x
- **結論**: 在 MoE 架構中，Embedding 層的查表操作佔用了大量頻寬卻幾乎沒有運算。透過將 Embedding Lookup 轉移到記憶體控制器內 (NMP)，我們成功避免了大量無效資料傳輸，達成 13.10x 的延遲改善。強烈建議在下一代架構中實作 NMP Embedding Lookup Engine。
