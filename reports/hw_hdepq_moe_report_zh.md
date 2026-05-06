# Auto-Researcher 分析報告：Hardware Dynamic Expert Pruning and Quantization (HDEPQ)

## 實驗背景
目前 MoE (Mixture of Experts) 模型在 Edge 裝置上推論時，面臨嚴重的 CPU-GPU 或 DRAM-SRAM 記憶體傳輸瓶頸。當 Router 分配多個 Experts (如 Top-2) 時，載入權重的頻寬消耗成倍增長。

## 解決方案 (HDEPQ)
我們提出並模擬了 **硬體動態專家剪枝與量化 (HDEPQ)** 架構。在此架構中：
1. Router 根據信心分數動態決定傳輸精度。
2. Top-1 Expert 維持 FP16 精度以確保基礎準確率。
3. Top-2 Expert 在 DMA 傳輸階段，由硬體自動進行 On-the-fly 的 INT4 降精度量化（4倍壓縮），大幅減少第二專家的記憶體頻寬佔用。

## 模擬數據 (hw_hdepq_moe_sim.py)
* **Baseline (純 FP16 傳輸) 延遲**: 4000.00 ms (1024 tokens)
* **HDEPQ 動態量化傳輸延遲**: 2500.00 ms
* **記憶體頻寬減少**: 37.50%
* **Throughput Speedup**: 1.60x

## 架構建議
建議在 Edge NPU 的 DMA 控制器中，整合「動態量化預測與轉換器 (Dynamic Quantization Converter)」，使硬體能根據 Token 的 Router 分數，無縫將次要專家權重壓縮傳輸，突破 PCIe/DRAM 頻寬牆。