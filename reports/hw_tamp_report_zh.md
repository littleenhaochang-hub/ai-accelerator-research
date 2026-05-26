# 硬體 Token 自適應 MoE 預取引擎 (HW-TAMP) 模擬報告

## 1. 研究背景
在 Mixture-of-Experts (MoE) 架構中，傳統的按需加載 (Demand Fetching) 必須等待 Router 計算完畢後才能開始從記憶體 (DRAM/NVMe) 拉取專家權重。這種循序相依性導致了嚴重的管線停頓 (Pipeline Stalls)，使得運算單元無法滿載。

## 2. 硬體架構創新 (HW-TAMP)
我們提出 **硬體 Token 自適應 MoE 預取引擎 (Hardware Token-Adaptive MoE Prefetcher, HW-TAMP)**：
- **超輕量預測器**：在 Token 進入主 Router 之前，先通過一個內建於 SRAM 介面的硬體極低精度 (如 2-bit) 分類器，提前預測最可能命中的專家。
- **非同步 DMA 拉取**：基於預測結果，立即觸發硬體 DMA 預先拉取專家權重，將記憶體延遲與主 Router 的完整矩陣運算完全重疊。

## 3. 實驗與驗證
透過 `hw_tamp_sim.py` 進行循環模擬：
- **Baseline (Demand Fetch)**: ~4118.81 ms
- **HW-TAMP (Prefetch)**: ~563.73 ms
- **延遲加速比 (Speedup)**: **7.31x**

## 4. 結論與建議
實驗證實，HW-TAMP 成功地將專家拉取延遲隱藏於 Router 運算背後，大幅減少了記憶體等待時間。
**建議**：將 HW-TAMP 引擎整合進 Edge NPU 的 DMA 控制器中，搭配超低延遲的預測查找表 (LUT)，以支援零停頓的超大 MoE 模型推理。