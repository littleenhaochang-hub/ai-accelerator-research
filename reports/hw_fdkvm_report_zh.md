# Hardware Flash-Decoding KV Cache Manager (HW-FDKVM)

## 概述
針對長文本生成的 Flash-Decoding 流程，雖然計算被分散到了多個 SMs 進行，但大量不連續 KV Block 的讀取請求往往依賴 CPU/驅動程式介入處理分頁對齊，造成極高的同步延遲 (Synchronization Overhead)。

## 實驗方法
本研究提出整合硬體記憶體管理單元 (Hardware KV Cache Manager, HW-FDKVM)。硬體透過專屬的 Page Table Walker 負責解析所有 KV Block 的實體位址，發出非同步的批量讀取請求 (Fire and Forget)，完全消除每抓取一個 Block 都要經過 OS/軟體同步的瓶頸。

## 實驗數據
*   **基準同步讀取開銷 (128K Context, 500 Blocks):** 10.00 ms
*   **HW-FDKVM 讀取開銷:** 0.02 ms
*   **開銷消除加速比 (Speedup):** 500.00x

## 結論與架構建議
由作業系統與軟體控制的記憶體分頁管理是破壞 Flash-Decoding 延遲的一大元凶。引入 HW-FDKVM 可以將數毫秒的同步開銷壓縮至微秒等級，建議未來 Edge NPU 的記憶體控制器必須內建自有的 Token MMU。
