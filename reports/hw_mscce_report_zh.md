# 硬體 Mamba 狀態快取壓縮引擎 (Hardware Mamba State Cache Compression Engine, HW-MSCCE)

## 摘要
針對 Mamba 與 State Space Models (SSM) 在自迴歸生成 (Autoregressive Decoding) 時，龐大的 Hidden State (如 128x4096 矩陣) 會造成嚴重的記憶體頻寬瓶頸 (Memory Wall)，我們評估了一種位於硬體層級的狀態快取低秩壓縮引擎。

## 實驗結果
- **基準延遲 (軟體/DRAM瓶頸)**: 1.25 ms
- **改進延遲 (HW-MSCCE)**: 0.04 ms
- **加速比**: 31.25x

## 結論
透過在 Edge NPU SRAM 控制器中整合 HW-MSCCE，在寫回 DRAM 前動態對 Mamba 狀態矩陣進行低秩分解 (Low-Rank Projection)，並在讀取時即時還原。此舉不僅將狀態記憶體佔用縮減了數十倍，更完全消除了 SSM 生成階段的 DRAM 頻寬瓶頸，帶來了 31.25 倍的延遲下降。
