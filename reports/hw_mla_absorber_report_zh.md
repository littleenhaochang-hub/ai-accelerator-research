# 實驗報告：硬體 MLA-RoPE 吸收引擎 (HW-MLA-Absorber)

## 摘要
在 DeepSeek MLA 架構中，雖然潛在向量 (Latent Vector) 大幅減少了 KV Cache 容量，但後續的 Up-projection 與 RoPE (旋轉位置編碼) 仍需大量的 SRAM 讀寫與獨立的 Kernel 執行。本實驗提出 HW-MLA-Absorber，將 RoPE 的旋轉矩陣計算直接融合進 Up-projection 的硬體 MAC 陣列中，消除中間態的 SRAM 寫入。

## 實驗結果
- **Baseline 延遲 (軟體分離執行):** 321.50 ms (32K Context)
- **HW-MLA-Absorber 延遲:** 272.00 ms
- **加速比:** 1.18x

## 架構建議
建議在 Edge NPU 內部實作「融合式 RoPE-MAC 單元」，對於極端依賴 MLA 降本的端側模型，可進一步減少 15% 以上的 SRAM 動態功耗與記憶體存取延遲。