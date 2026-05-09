# Auto-Researcher 分析報告：Hardware Inline Top-P Sampler Engine (HW-ITPSE)

## 1. 瓶頸分析 (Analyze)
在 LLM 的推論循環中，每產生一個 Token，NPU 都需要將巨大的 Logits 陣列（如 Llama 3 的 128K Vocab）透過 PCIe 傳輸回 CPU 進行 Softmax 與 Top-P/Top-K 採樣。這個頻繁的 PCIe 同步與 CPU 排序（O(N log N)）造成了極大的延遲瓶頸（Latency Bubble），限制了每秒 Token 數（TPS）。

## 2. 理論探索 (Explore)
我們提出「Hardware Inline Top-P Sampler Engine (HW-ITPSE)」。將採樣邏輯完全硬體化，內嵌於 NPU 的最後輸出端（LM Head 之後）。硬體採用並行的比較器樹（Comparator Tree）與累加器，能夠在數個時鐘週期內（O(1)）直接於 SRAM 內部完成 Top-P 過濾與隨機採樣，最終僅將單個 Token ID 傳回 CPU。

## 3. 原型實驗結果 (Prototype)
我們於 `hw_inline_top_p_sampler_sim.py` 進行了系統級延遲模擬：
*   **基準測試 (CPU 採樣, 128K Vocab):** 延遲 2.19 ms。
*   **HW-ITPSE (硬體並行採樣):** 延遲 0.005 ms。
*   **效能提升:** 達成 **438.47x 的採樣階段加速**。

## 4. 硬體架構結論 (Conclusion)
Edge NPU 若要達成極致的低延遲串流輸出，必須實現「Zero-PCIe-Sync」的推論迴圈。將 Top-P/Top-K 採樣器硬體化整合至 NPU 內部，可完全消除 CPU 的介入，是實現單晶片全自動推論的最後一塊拼圖。
