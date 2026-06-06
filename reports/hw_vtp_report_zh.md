# 硬體視覺 Token 剪枝器 (HW-VTP) 實驗報告

## 1. 瓶頸分析
根據 `ai-accelerator-research/RESEARCH_REPORT.md`，當前 Edge NPU 處理視覺語言模型 (VLM) 時，長文本 Prefill OOM 與算力瓶頸十分嚴重。圖像轉換為 Token 後（例如 16K Context），其中包含大量無用的背景 Patch（如純色天空、空白牆壁）。若將這些 Token 全部送入 Transformer MAC 陣列，將浪費大量算力與動態功耗。

## 2. 探索文獻
參考最新的 ICML 論文，關於動態 Token 丟棄（Token Dropping）與視覺 Token 稀疏性。我們提出硬體層級的 **Hardware Visual Token Pruner (HW-VTP)**，透過在 SRAM 讀取端口設置輕量級特徵評估器，直接在硬體層面過濾掉背景 Token。

## 3. 建立原型並驗證
我們使用 `hw_vtp_sim.py` 驗證了 HW-VTP 的效能：
*   **基準線 (Dense Prefill):** 5.4976 ms
*   **HW-VTP (Prune 75%):** 1.4744 ms
*   **Latency Speedup:** 3.73x
*   **Dynamic Energy Reduction:** 75.00%
*   **SQNR:** 31.5 dB (保持視覺特徵)

## 4. 結論
透過硬體與軟體協同設計，HW-VTP 能在近乎零軟體開銷的情況下，大幅提升邊緣設備處理高解析度圖像的能力。強烈建議將此架構整合至下一代 Agentic AI 終端晶片的 DMA 控制器中。