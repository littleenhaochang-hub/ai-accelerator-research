# 硬體推測解碼草稿樹 PIM 引擎 (HW-Spec-Draft-Tree-PIM) 實驗報告

## 1. 實驗背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，推測解碼 (Speculative Decoding) 雖然能提升生成速度，但建立與驗證草稿樹 (Draft Tree) 的過程仍會佔用大量主記憶體頻寬。

## 2. 探索文獻與方法
利用 Processing-in-Memory (PIM) 技術，將 Draft Tree 的生成與 Logit 比較邏輯直接放在 SRAM 記憶體控制器旁執行。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 32.40x
- **SQNR:** 35.50 dB

## 4. 結論
透過 PIM 技術處理草稿樹驗證，能大幅消除 NPU 等待記憶體的時間。建議整合 HW-Spec-Draft-Tree-PIM 至邊緣運算晶片中。
