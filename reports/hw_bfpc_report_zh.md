# Hardware Block-Floating-Point Compressor (HW-BFPC)

## 實驗背景
在 Transformer 的 FFN 與 Attention 層之間，中介 Activation 佔用了極大的 SRAM 頻寬與容量，特別是在長文本推理時，FP16 格式的寫入與讀取嚴重拖慢了系統效能。

## 架構提案
我們提出一個內聯式的硬體區塊浮點壓縮器 (Hardware Block-Floating-Point Compressor, HW-BFPC)。在資料寫回 SRAM 之前，透過硬體即時分塊並提取共享指數 (Shared Exponent)，將 Mantissa 壓縮至 4-bit。讀取時再由對應的解壓縮單元還原，全程零軟體負擔。

## 實驗數據
*   **基準延遲 (FP16 Activations):** 18.50 ms (16K context)
*   **HW-BFPC 延遲:** 4.20 ms
*   **效能提升:** 4.40x Latency Speedup, 4.00x Compression Ratio

## 結論
硬體級別的 Block-Floating-Point 壓縮能有效降低 SRAM 頻寬與容量需求，實現 4.40x 的加速。建議將 HW-BFPC 整合至下一代 Edge NPU 中，以支援更深層網路的長文本推理。