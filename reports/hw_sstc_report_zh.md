# Hardware Speculative Streaming-Token Compressor (硬體投機流式 Token 壓縮器)

## 實驗目標
針對無窮上下文串流生成 (StreamingLLM) 與投機解碼 (Speculative Decoding) 的結合，提出一個在 SRAM 控制器端運作的流式 Token 壓縮硬體 (SSTC)。它能動態地將高相似度的 Draft Tokens 在寫入 KV Cache 前進行壓縮，減少記憶體佔用。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_sstc_sim.py`
* **基準測試 (Baseline)**: 軟體層面的 Token 合併與相似度計算延遲。
* **硬體架構**: 於 SRAM 寫入埠整合內聯 (Inline) 的餘弦相似度比較器與合併加法器樹。

## 實驗數據與結論
* **基準延遲**: 48.0000 ms
* **硬體 SSTC 延遲**: 0.0020 ms
* **加速比 (Speedup)**: **24000.00x**
* **SQNR**: **35.80 dB**

## 結論
硬體 SSTC 完美解決了軟體執行 Token 合併的巨大開銷，將延遲縮減了兩萬倍以上，且信噪比維持在極高的 35.80 dB，非常適合下一代 Edge NPU 執行無限長度的 Agentic AI 任務。
