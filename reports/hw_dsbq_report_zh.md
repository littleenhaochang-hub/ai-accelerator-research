# Hardware Dynamic Sub-Byte Quantization (HW-DSBQ)

## 實驗背景 (Background)
即使使用 4-bit 量化，7B 級別的大語言模型在 Edge 裝置上仍受限於 LPDDR 的記憶體頻寬瓶頸 (Memory Wall)。

## 實驗設計 (Methodology)
本實驗設計了針對 1.58-bit (Ternary 權重) 的硬體級解壓縮單元 (`hw_dsbq_sim.py`)。透過在 NPU 的 SRAM 讀取埠部署內聯解壓縮引擎 (Inline Decompression Engine)，將權重以緊湊的 1.58-bit 格式儲存於 DRAM，並在讀取時瞬間還原。

## 實驗結果 (Results)
- INT4 Fetch Latency (7B model): 0.0350 s
- HW-DSBQ 1.58-bit Latency: 0.0153 s
- **Speedup**: 2.28x 

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 的 Memory Controller 端整合「HW-DSBQ 引擎」，以原生支援 BitNet 等 1.58-bit 網路架構，將記憶體頻寬需求降低約 60%，徹底打破 Edge AI 的記憶體傳輸瓶頸。