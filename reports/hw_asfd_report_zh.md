# Hardware Asynchronous Speculative Fetching Engine (HW-ASFD) 實驗報告

## 背景與瓶頸分析
在推論框架中使用 Speculative Decoding (投機解碼) 時，通常需要一個小型的 Draft Model 來預測接下來的數個 Token，再交由龐大的 Target Model 進行驗證。傳統架構下，這兩者的協調高度依賴 CPU 軟體排程：Draft Model 運算完後，Token 須傳回 CPU 進行驗證準備，再發起 Target Model 的 Kernel。這種軟體中斷與 PCIe 往返大幅抵銷了投機解碼帶來的延遲優勢。

## 解決方案：HW-ASFD (硬體非同步投機抓取引擎)
我們提出 **HW-ASFD**，這是一種內嵌於 NPU 控制器中的非同步同步器。
HW-ASFD 允許 Draft Model 與 Target Model 在 NPU 的不同區塊 (或 Chiplets) 平行執行。Draft Model 產生的 Token 直接透過硬體 FIFO 佇列傳遞給 Target Model 的驗證單元，完全繞過 CPU。更重要的是，當 Target Model 正在驗證當前 Draft 時，Draft Model 已經開始非同步抓取下一輪的推測 Token。

## 實驗結果
透過 Python 模擬 (`hw_asfd_sim.py`)，針對 1024 Token 序列 (每次 Draft 4 Tokens) 進行測試：
- **基準延遲 (軟體投機排程):** 1587.20 ms
- **HW-ASFD 延遲 (硬體非同步抓取):** 1036.80 ms
- **吞吐量加速比 (Speedup):** 1.53x

## 結論
HW-ASFD 透過消除 CPU 介入與實現 Draft/Target 模型在 NPU 內部的 Pipeline 重疊，為 Speculative Decoding 帶來 1.53 倍的額外加速。這項硬體與演算法的深度結合，使 Edge 裝置能真正享受投機解碼帶來的極致低延遲。
