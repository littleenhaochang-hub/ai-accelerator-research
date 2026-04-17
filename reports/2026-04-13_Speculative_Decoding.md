# Auto-Researcher 實驗報告：Speculative Decoding (投機解碼) 硬體加速架構
**日期:** 2026-04-13

## 1. 瓶頸分析
根據 `RESEARCH_REPORT.md` 的規劃，當我們試圖在 Edge NPU 上執行大型 LLM (Target Model) 時，Auto-Regressive 的 Decoding 階段由於是 sequential 的，無法充分利用龐大的硬體平行運算資源 (Under-utilization)。這導致 Memory Bandwidth 成為瓶頸，Compute 資源閒置。

## 2. 文獻探索
從 arXiv 2025/2026 以及 ICML/ICLR 中，針對 Speculative Decoding 的硬體發展包含：
*   **SPEQ (arXiv 2025/10):** 使用 bit-sharing 量化，直接從原本的 FP16/BF16 模型中抽出 4-bit 的 Draft Model，減少儲存負擔。
*   **FSD-Acc (IEEE 2026/02):** 提出 Fused Speculative Decoding (FSD) 硬體加速器，將所有運算統一為通用的矩陣相乘 (GEMM)，使 Draft 與 Target model 之間能夠共享權重與暫存器，避免頻繁的外部記憶體存取。
*   **Parallel Speculative Decoding (ICLR 2026):** 解決 Draft 與 Target model 之間「互相等待 (mutual waiting)」的延遲問題。

## 3. Prototype 驗證
我們編寫 `spec_decoding_prototype.py` 來驗證 Speculative Decoding 的週期性行為。
*   假設 Target Model 生成 1 token 需要 15ms，Draft Model 需要 2ms，Verification 批次處理需要 16ms。
*   參數 $\gamma = 4$ 且預測接受率為 70%。
*   **驗證結果:** 原本 100 token 需要 1500 ms 的 Auto-regressive 生成，經由投機解碼只需 864 ms (約 36 個 parallel steps)。
*   **加速比: 1.74x**（無損生成品質）。

## 4. 結論
要在硬體層級最大化 Speculative Decoding 的效益，未來的 Accelerator 不應將 Draft 和 Target 切割在不同的物理晶片上。我們必須設計 **Reconfigurable PE Arrays (可重構運算陣列)**，能支援如 FSD-Acc 的權重共享 (Weight Sharing) 機制，確保 Draft 預測與 Target 驗證階段之間的 Context 與 KV Cache 轉換是 zero-copy 的。此研究已納入我們下一代硬體架構的開發指引中。
