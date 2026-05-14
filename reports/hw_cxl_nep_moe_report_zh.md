# 硬體 CXL-NVDIMM 專家預取器 (HW-CXL-NEP) 模擬報告

## 1. 瓶頸分析
目前的 MoE (Mixture of Experts) 推論在邊緣裝置上，主要受限於專家權重從 NVMe 透過 PCIe 經 CPU RAM 傳輸到 NPU 的頻寬與延遲 (Memory Wall)。

## 2. 解決方案 (Hardware CXL-Attached NVDIMM Expert Prefetcher)
我們提出將專家權重存放在支援 CXL 3.0 的 NVDIMM 中，並在 NPU 內建硬體預取器 (Hardware Prefetcher)。該硬體模組透過觀察前面層的 token 路由軌跡，提前將預測的專家權重經由 CXL Memory Semantics 直接 Mapping 至 NPU SRAM，完全繞過 CPU 與傳統 OS Block 驅動的介入。

## 3. 實驗結果
透過 `hw_cxl_nep_moe_sim.py` 模擬 1000 個 token 的解碼過程：
- Baseline (PCIe NVMe Fetching): 3.0000s
- HW-CXL-NEP (Hardware Prefetching): 0.7464s
- **Speedup: 4.02x**

## 4. 架構建議
針對次世代 Edge NPU，建議整合「CXL 3.0 硬體預取引擎」，直接管理外部 NVDIMM 的存取，確保 MoE 推論時間完全由 Compute 決定，而非被 PCIe I/O 阻塞。