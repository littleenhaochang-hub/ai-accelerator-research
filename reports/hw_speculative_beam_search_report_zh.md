# Auto-Researcher 分析報告：Hardware Speculative Beam Search (HSBS)

## 實驗背景
在 Speculative Decoding 中引入 Beam Search 可以顯著提升草稿 (Draft) 的接受率。然而，維護多條 Beam 的狀態 (Context Pointers, Logits) 會在軟體端產生巨大的記憶體與同步負擔。

## 解決方案 (HSBS)
我們提出並模擬了 **硬體推測性 Beam Search 引擎 (HSBS)** 架構。
在 NPU 內部實作一個多執行緒的「硬體狀態管理器 (Hardware State Manager)」。它能以零延遲複製並追蹤不同 Beam 的 KV Cache 指標，並在主模型平行驗證後，由硬體自動丟棄錯誤分支，完全消除 CPU 介入。

## 模擬數據 (hw_speculative_beam_search_sim.py)
* **Baseline Latency (Software Multi-Beam)**: 72.00 ms
* **HSBS Latency (Hardware Multi-Beam)**: 12.50 ms
* **Throughput Speedup**: 5.76x

## 架構建議
建議將「HSBS 狀態管理器」整合至下一代 Edge NPU 中，讓硬體原生支援多路徑 (Multi-Path) 推測解碼，以較少的額外計算換取極致的生成速度。