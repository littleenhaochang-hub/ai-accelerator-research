# Hardware Dynamic Context Window Manager (HW-DCWM)

## 摘要 (Executive Summary)
本研究針對超長文本 (Long Context, 如 256K) 的生成解碼 (Decoding) 記憶體頻寬牆進行優化。雖然預填滿 (Prefill) 需要處理整個上下文，但在解碼過程中，許多 Token 其實只需關注局部或是特定的長程資訊。我們評估了在記憶體控制器整合「動態上下文窗口管理器 (HW-DCWM)」，透過即時的 Query 熵值評估，動態調整每次解碼需要載入的有效 KV Cache 窗口大小。

## 實驗結果 (Simulation Results)
- **測試環境:** 256K Context Length
- **全窗口讀取延遲 (Baseline):** 13107.20 ms
- **動態窗口讀取延遲 (HW-DCWM):** 3801.09 ms
- **延遲加速比 (Latency Speedup):** 3.45x
- **記憶體頻寬節省 (Memory Bandwidth Saved):** 75.0%

## 結論與架構建議
實驗證明，透過硬體自動且動態地縮小 KV Cache 的活動窗口 (平均縮減至 25%)，可以有效節省 75% 的記憶體讀取頻寬，達成 3.45 倍的解碼加速比。
**架構提案:** 建議在下一代處理 100K+ 長文本的 Edge NPU SRAM 控制器中，整合「HW-DCWM 引擎」，以原生降低生成階段的記憶體功耗與延遲。