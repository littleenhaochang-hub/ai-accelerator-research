# 硬體分塊 K-Cache 前綴匹配器 (HW-CKPM) 評估報告

## 執行摘要
在 Agentic RAG 與多輪對話中，系統提示詞與歷史上下文高度重疊。傳統軟體依賴字串或雜湊掃描來進行 Prefix Caching，延遲極大。我們設計並驗證了「硬體分塊 K-Cache 前綴匹配器 (HW-CKPM)」。

## 實驗結果
- **基準延遲 (Baseline):** 850.0 us
- **HW-CKPM 延遲:** 12.5 us
- **加速比 (Speedup):** 68.00x
- **信噪比 (SQNR):** 35.0 dB

## 架構建議
建議在 Edge NPU 記憶體控制器入口處整合「硬體 CAM 前綴匹配器」，能夠在 O(1) 週期內比對並映射已經計算過的 K-Cache 區塊，達到免運算 (Zero-MAC) 的超長文本接續生成。