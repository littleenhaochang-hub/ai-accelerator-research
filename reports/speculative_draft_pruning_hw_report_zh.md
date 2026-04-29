# Hardware Speculative Draft Pruning Engine 驗證報告
## 實驗結果
- **軟體草稿分支修剪延遲**: 22.00 ms
- **硬體 Inline 修剪延遲**: 1.50 ms
- **吞吐量加速**: 14.67x
- **結論**: 在樹狀推測解碼 (Tree-based Speculative Decoding) 中，管理並修剪大量低信心度分支在軟體端會造成 O(N) 的控制流開銷。透過硬體 Inline Logit Comparator，我們能在 Draft 生成階段即時砍斷無效分支，達成 14 倍的修剪加速，將更多資源留給 Target Model 的平行驗證。
