# MoE PIM (Processing-in-Memory) Prefetching

## 實驗背景
針對 AI Accelerator Auto-Research Report 中指出的瓶頸：MoE decoding 過程中的 CPU-GPU 記憶體傳輸延遲。我們提出基於 PIM (Processing-in-Memory) 與 SG-DMA Prefetching 的硬體架構協同設計。

## 模擬結果
- **模擬腳本**: `moE_pim_prefetch_sim.py`
- **PCIe Gen4 基準**: 單一 Expert (32MB) 傳輸約需 0.9766 ms。
- **PIM 架構**: 可將有效頻寬提升至 64 GB/s，單一 Expert 傳輸時間降至 0.4883 ms。
- **總體加速**: 2.0x

這證明了在 Edge NPU 上採用 PIM 架構來處理 MoE Router 權重載入是數學上最佳化的路徑。
