# Hardware Top-P/Top-K Sampler 模擬報告

## 摘要
本報告探討在自迴歸解碼 (Autoregressive Decoding) 階段，將 Top-P/Top-K 抽樣邏輯從 CPU 轉移至 NPU 輸出的專屬硬體單元，以消除每個 Token 產生時的 PCIe 同步與傳輸延遲。

## 實驗設計
- 詞表大小 (Vocab Size) 設為 128,256 (如 Llama-3)。
- 軟體延遲包含將 Logits 透過 PCIe 傳回 CPU、排序、Softmax 與抽樣；硬體延遲基於 NPU 內建的平行排序網路與硬體亂數產生器 (PRNG)。

## 實驗結果
- **SW Latency (CPU + PCIe)**: 6.91 ms
- **HW Latency (On-Chip)**: 0.13 ms
- **Speedup**: 53.90x

## 架構建議
在傳統架構中，每一次產生 Token 都需要將十幾 MB 的 Logits 傳回 CPU 進行抽樣，這會導致極高的 PCIe 往返延遲，嚴重拖慢 Decode TPS。建議在 Edge NPU 的輸出暫存器旁直接整合「Hardware Sampler Engine」，以實現 Zero-PCIe-Sync 的極速生成迴圈。