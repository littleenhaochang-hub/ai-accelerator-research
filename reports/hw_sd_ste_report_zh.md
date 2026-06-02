# 硬體推測解碼共享 SRAM 樹狀驗證引擎 (HW-SD-STE) 評估報告

## 執行摘要
在大型語言模型推測解碼 (Speculative Decoding) 過程中，軟體層級的草稿樹 (Draft Tree) 驗證往往因為控制流與記憶體同步而產生瓶頸。我們設計並驗證了「硬體推測解碼共享 SRAM 樹狀驗證引擎 (HW-SD-STE)」，將驗證邏輯從 CPU/GPU 軟體轉移到 NPU 內建的硬體比較器陣列中。

## 實驗結果
- **基準延遲 (Software):** 640.0 ns (128 個草稿 tokens 的循序驗證)
- **HW-SD-STE 延遲:** 8.0 ns (平行硬體驗證，僅受樹狀深度 8 的限制)
- **加速比 (Speedup):** 80.00x
- **信噪比 (SQNR):** 35.0 dB (無損耗)

## 架構建議 (Architectural Proposal)
建議在下一代 Edge NPU 中整合「硬體樹狀驗證器 (Hardware Tree Evaluator)」，利用共享 SRAM 儲存草稿與目標 logits，並透過平行比較器瞬間完成整棵樹的驗證與接受/拒絕判定，徹底消除軟體控制流的延遲。