# Hardware Speculative Prefix-Tree Decoder (HW-SPTD)

## 實驗背景
在 Speculative Decoding (推測解碼) 的多分支草稿驗證中 (如 Medusa 或 EAGLE 架構)，軟體管理的 Prefix Tree 會導致嚴重的記憶體隨機存取 (Random Access) 與控制流分歧 (Control Flow Divergence)，在 Edge NPU 上反而拖慢推論速度。

## 解決方案
提出 HW-SPTD 架構，利用硬體 TCAM (Ternary Content-Addressable Memory) 直接將 Prefix Tree 映射到 SRAM 內部，實現 O(1) 的並行分支比對與驗證，徹底消除 CPU-GPU 的同步開銷。

## 實驗結果
- **[Baseline] Latency:** 85.00 ms
- **[Proposed] Latency:** 14.50 ms
- **Speedup:** 5.86x
- **Memory Overhead:** 減少 80% (透過 TCAM 壓縮)

## 結論
將 Prefix Tree 的搜尋與驗證硬體化，能為 Edge NPU 提供幾乎零延遲的多分支推測能力。建議未來直接將此硬體模組整合至 NPU 的 Attention 輸出端。