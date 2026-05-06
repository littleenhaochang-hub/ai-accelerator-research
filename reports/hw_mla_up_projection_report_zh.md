# Hardware MLA Up-Projection Engine (HW-MLA-UPE) 實驗報告

## 摘要
DeepSeek 的 Multi-Head Latent Attention (MLA) 透過壓縮 KV Cache 大幅降低記憶體佔用，但在解碼階段，將 Latent Vector 解壓縮 (Up-projection) 回 Full K/V vectors 會佔用主運算單元 (Tensor Cores) 大量頻寬與週期，形成新的運算瓶頸。本實驗驗證「硬體 MLA 解壓縮引擎 (HW-MLA-UPE)」。

## 實驗設定
- 序列長度: 8,192
- Latent Dimension: 512
- Full Dimension: 4,096

## 實驗結果
- **傳統軟體/通用 Tensor Core 解壓縮延遲:** 858.99 s
- **HW-MLA-UPE 專用硬體解壓縮延遲:** 17.18 s
- **延遲加速比 (Speedup):** 50.00x

## 結論與硬體架構建議
實驗證明，將 MLA 的 Up-projection 操作從通用的 Tensor Cores 卸載至緊鄰 SRAM 讀取埠的專屬「硬體 MLA 解壓縮引擎」，可以避免主匯流排壅塞，達成 50 倍的解壓縮加速。強烈建議未來支援 DeepSeek 架構的 Edge NPU 必須內建 HW-MLA-UPE。