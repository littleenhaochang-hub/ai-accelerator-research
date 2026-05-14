# Hardware Dynamic KV Quantization (HW-DKVQ)

## 實驗背景 (Background)
處理 128K 超長文本時，即使使用 4-bit 量化，KV Cache 仍佔用極大頻寬與容量。

## 實驗設計 (Methodology)
本實驗設計了硬體級的動態混合精度管理器 (`hw_dkvq_sim.py`)。對於注意力分數低的背景 Token 使用 1-bit (極低精度) 壓縮，對於 Heavy Hitters 則保留 4-bit。硬體直接在讀取時動態還原精度，無須軟體介入。

## 實驗結果 (Results)
- Static 4-bit KV Latency (128K, BS=16): 0.3436 s
- HW-DKVQ Dynamic Latency: 0.1379 s
- **Speedup**: 2.49x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU SRAM 控制器中整合「HW-DKVQ 引擎」，根據硬體 Attention Score 預測器，動態決定寫入與讀取的位元數，大幅突破長文本生成的記憶體牆。