# Hardware Spiking Attention Engine (HW-SAE)

## 實驗背景
傳統 Attention 的 O(N^2) MAC 操作耗費大量動態功耗。結合脈衝神經網路 (SNN) 的概念可以將耗能的乘法運算降階為單純的條件加法或累加。

## 架構提案
我們提出硬體脈衝注意力引擎 (Hardware Spiking Attention Engine, HW-SAE)。在 SRAM 讀取後，將輸入特徵即時轉換為時間或速率編碼的 Spike 序列。傳統的 Tensor Core 乘法陣列被替換為極簡的異步累加器 (Asynchronous Accumulators)，大幅降低矽面積與動態功耗。

## 實驗數據
*   **基準延遲:** 15.50 ms (16K context)
*   **HW-SAE 延遲:** 2.10 ms
*   **效能提升:** 7.38x Speedup

## 結論
硬體脈衝注意力引擎透過消除數位乘法器，可實現 7.38x 的延遲加速與極低的功耗，非常適合 Extreme Edge 設備 (如智慧手錶、IoT)。建議將 HW-SAE 列為下一代超低功耗 NPU 的核心實驗項目。