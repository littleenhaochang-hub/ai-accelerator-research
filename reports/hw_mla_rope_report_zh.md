# Hardware MLA-RoPE Engine (HW-MLA-RoPE) 實驗報告

## 背景與瓶頸分析
近期 DeepSeek 架構提出的 Multi-Head Latent Attention (MLA) 透過將 KV Cache 壓縮為 Latent Vector ($c_t$) 來大幅減少 DRAM 容量佔用。然而，當模型在 Edge NPU 上執行時，需要先將 Latent Vector 解壓縮 (Up-Projection) 成原始的 Key，再對其應用 Rotary Position Embedding (RoPE)。傳統軟體執行方式會將解壓縮後的龐大 Key 矩陣先寫回 SRAM，再讀取出來進行 RoPE 計算，造成 SRAM 頻寬的無謂浪費。

## 解決方案：HW-MLA-RoPE
我們提出將 CORDIC 旋轉引擎直接串聯在 MLA 的 Up-Projection 硬體單元之後（**HW-MLA-RoPE**）。當 Latent Vector 從 SRAM 讀出並經過 MAC 陣列解壓縮後，資料直接流入硬體 RoPE 引擎，完成旋轉後再進入 Attention 點積單元。這完全消除了高維度 (如 4096-dim) Key 矩陣的 SRAM Read/Write 往返。

## 實驗結果
透過 Python 模擬 (`hw_mla_rope_sim.py`)，針對 8K Context 進行測試：
- **傳統分離式 Latency:** 0.5713 ms
- **HW-MLA-RoPE Latency:** 0.5042 ms
- **吞吐量加速比 (Speedup):** 1.13x
- **SRAM R/W Latency 節省:** 0.0671 ms (徹底消除了中間層的 SRAM 讀寫頻寬浪費)

## 結論
儘管整體加速比 (1.13x) 看似不大，但 HW-MLA-RoPE 從根本上解決了 SRAM 內部頻寬 (Internal Bandwidth) 擠兌的問題。這使得 Edge NPU 能夠將釋放出來的 SRAM 頻寬用於同時並行的其他 Token 解碼或 Draft 模型推論。建議將此 Inline CORDIC 架構作為下一代支援 DeepSeek-V3/R1 類架構的標準硬體配置。
