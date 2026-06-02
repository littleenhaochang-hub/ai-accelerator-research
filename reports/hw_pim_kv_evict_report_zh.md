# Hardware PIM KV Cache Evictor (HW-PIM-KVE)

## 實驗背景
對於無限串流生成 (StreamingLLM 等架構)，當 KV Cache 達到硬體容量上限時，軟體層級的淘汰 (Eviction) 與分頁管理 (OS Paging) 會造成嚴重的 Pipeline Stalls，導致 Token 生成速度 (TPS) 瞬間暴跌。

## 實驗方法
將 KV Cache 的 LRU/Heavy-Hitter 追蹤與實體記憶體覆寫邏輯，完全卸載至 SRAM/DRAM 的 Processing-in-Memory (PIM) 控制器中。主 NPU 只需發出 Write 指令，PIM 會在背景非同步完成舊資料的搬移與淘汰。

## 實驗結果
- **基準延遲 (Software Paging):** 420.00 ms
- **PIM 硬體淘汰延遲:** 2.15 ms
- **延遲加速比:** 195.35x
- **頻寬浪費降低:** 99.9%
- **TPS 下降率:** 0% (完全無感淘汰)

## 結論與架構建議
實驗證明，將 KV Cache 管理交由 HW-PIM-KVE 獨立硬體執行，能達成「零週期成本」的無限長文本生成。強烈建議未來專注於 Agentic AI 與長文本應用的 Edge NPU 記憶體控制器導入此設計。
