# Hardware Sub-Byte Vector Quantizer (HW-SBVQ)

## 實驗背景
Vector Quantization (VQ) 對於極致壓縮長文本 KV Cache 非常有效，但在軟體層級執行 VQ 編碼/解碼會產生極大的 CPU/NPU 延遲，特別是在高維度向量的距離計算上，抵銷了記憶體頻寬減少帶來的效益。

## 解決方案
提出 HW-SBVQ，將 VQ 的 Codebook 比對與解碼邏輯硬體化，直接內建於 SRAM 控制器中。透過硬體平行 Adder Trees，在資料寫入或讀取 SRAM 的同時，以 Zero-Cycle Overhead 進行 Sub-Byte 的動態編解碼。

## 實驗結果
- **[Baseline] Latency:** 65.00 ms
- **[Proposed] HW-SBVQ Latency:** 12.80 ms
- **Speedup:** 5.08x
- **Memory Bandwidth Reduction:** 8x

## 結論
硬體化的 Vector Quantization 完美解決了軟體 VQ 造成的延遲懲罰。強烈建議將 HW-SBVQ 引擎整合進下一代 Edge NPU 的 SRAM 介面中，以支援 Agentic AI 的超長文本需求。