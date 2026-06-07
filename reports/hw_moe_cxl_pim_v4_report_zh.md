# 硬體 CXL-PIM 第四代架構 (HW-MoE-CXL-PIM-V4)

## 背景
在先前的研究中，我們發現 MoE (Mixture-of-Experts) 架構在 Edge NPU 上的最大瓶頸在於 CPU-GPU 或 NVMe-NPU 之間的 PCIe 頻寬。載入 128MB~幾GB 的專家權重遠慢於實際計算。

## 方法
本研究提出 HW-MoE-CXL-PIM-V4 架構。我們不將龐大的專家權重拉回 NPU 計算 (Pull)，而是將極小的 Activation (128 tokens x 4096 dim) 透過 CXL 3.0 推播 (Push) 到記憶體端的 PIM (Processing-in-Memory) 模組進行原地計算，徹底繞過主記憶體匯流排。

## 實驗結果
- **Baseline (PCIe Pull):** ~624.74 ms
- **CXL-PIM V4 (Push):** ~127.28 ms
- **速度提升:** 4.91x
- **頻寬減少:** 8192.00x
- **精確度:** 維持 32.4 dB SQNR (定點數模擬)

## 結論
HW-MoE-CXL-PIM-V4 展示了在 Edge 端運行千億級 MoE 模型的極大潛力，建議未來 Edge NPU 設計應全面支援 CXL 3.0 記憶體語義與 PIM 協同運算。