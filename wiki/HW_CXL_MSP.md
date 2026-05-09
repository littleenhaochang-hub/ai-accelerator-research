# Hardware CXL 3.0 MoE Speculative Prefetching (HW-CXL-MSP)

## 實驗背景
針對 MoE 解碼期間的 CPU-GPU 記憶體傳輸瓶頸，傳統 PCIe 匯流排的 DMA overhead 嚴重拖慢了吞吐量。

## 架構設計
透過 CXL 3.0 的記憶體語義協定，整合了硬體級別的 Speculative Prefetcher，能夠在不干預主 Tensor Core 運算的情況下，非同步提取未來的專家權重。

## 模擬結果
*   **基準 (PCIe Gen4 Demand):** 2560 ms (1024 tokens)
*   **HW-CXL-MSP:** 512 ms (1024 tokens)
*   **總結提升:** 5.00x 吞吐量加速。

建議將此設計列入 Edge NPU 規格，解決 MoE 的 Memory Wall。
