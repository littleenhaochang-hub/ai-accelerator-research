# 長文本 Prefill OOM 解決方案：Chunked Prefill 與 INT4 KV Cache 協同設計

## 瓶頸分析
根據 `ai-accelerator-research/RESEARCH_REPORT.md` 與近期邊緣裝置 (Mac mini 16GB) 的測試，在處理超過 32K 長度的文本時，Prefill 階段遭遇嚴重的 Out-Of-Memory (OOM) 崩潰。這主要源於兩個物理限制：
1. **$O(N^2)$ 注意力矩陣爆發：** 在 32K 長度下，標準 Attention 矩陣需佔用高達 64GB 記憶體。
2. **KV Cache 線性增長：** 32K Token 的 FP16 KV Cache 需佔用約 16GB，直接耗盡 Mac mini 所有的統一記憶體 (Unified Memory)。

## 探索文獻與架構設計
我們回顧了最新的 arXiv 與系統頂會論文 (FlashAttention-3, Ring Attention, 等)，提出以下硬體-軟體協同解決方案：
1. **Chunked Prefill (區塊化預填充)：** 將無限長的 Context 拆分為固定大小 (例如 4096) 的 Chunk 進行遞迴計算，這將注意力矩陣的記憶體佔用從 $O(N^2)$ 強制降至 $O(B \times C^2)$，在我們的模擬中，Attention 記憶體可從 64GB 驟降至固定的 1GB。
2. **INT4 KV Cache 壓縮：** 即使使用了 Chunked Prefill，32K 的 KV Cache 仍然高達 16GB。必須引入我們實驗室開發的 TurboQuant 或 KIVI (4-bit KV Cache 壓縮技術)，將 KV Cache 佔用從 16GB 砍至 4GB，確保整體 Prefill 過程可以完全塞入邊緣設備的 SRAM/統一記憶體中。

## Prototype 驗證
我們撰寫了 `ai-accelerator-research/prefill_oom_sim.py` 進行了硬體資源模擬：
- **8K 文本：** 標準模式需 8GB (勉強通過)，Chunked 模式需 5GB。
- **32K 文本：** 標準模式需 80GB (必定 OOM)，Chunked + FP16 模式需 17GB (OOM)。
- **32K 文本 + INT4 KV Cache (預估)：** Chunked (1GB) + INT4 KV (4GB) = 5GB，安全通過。

## 結論
長文本 Prefill OOM 的終極解法是 **Chunked Prefill + Sub-4-bit KV Cache** 的混合架構。我們下一步將會把 4-bit KV 壓縮演算法的 Pytorch 實作與 Chunked 引擎整合。
