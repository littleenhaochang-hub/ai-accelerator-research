# StreamingLLM Attention Sink 硬體驅逐機制分析

## 實驗背景
在多輪對話與無限長文本生成（如 AI Agent 循環）中，標準的 KV Cache 記憶體佔用會無止盡地增長（$O(N^2)$ 的讀取量），最終導致 DRAM 耗盡與推論速度崩潰。我們參考 StreamingLLM 的 Attention Sink 概念，進行硬體層級的 KV Cache 自動驅逐 (Eviction) 模擬。

## 實驗方法
撰寫 `streaming_llm_eviction_sim.py`，模擬生成 100,000 個 Tokens 的極端情況。
- **Baseline (Dense Attention)**: 儲存並讀取所有歷史 Tokens 的 KV。
- **StreamingLLM**: 僅保留最初的 4 個 Attention Sink Tokens 與最近的 2048 個 Sliding Window Tokens。

## 實驗數據
- **Dense Attention KV Reads**: 81.92 TB
- **StreamingLLM KV Reads**: 3.33 TB
- **KV Memory Bandwidth Reduction**: 95.94%

## 硬體架構結論
StreamingLLM 機制在 100K 序列生成的場景下，能省下近 96% 的記憶體頻寬，並使記憶體容量需求保持常數（不隨生成長度增加）。
為了達成零成本的動態管理，未來的 Edge NPU 記憶體控制器內應當實作 **SRAM Ring Buffer with Static Sink Roots (帶有靜態 Sink 根節點的 SRAM 環狀緩衝區)**。硬體應自動覆寫過期的 Sliding Window 區塊，同時鎖死並保護最前面的 Sink 區塊，以徹底消除軟體層面的 Memory Management 開銷。
