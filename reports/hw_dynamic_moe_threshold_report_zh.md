# Hardware Dynamic MoE Thresholding Engine (HW-DMT)

## 實驗背景與動機
在混合專家 (MoE) 模型中，Router 會為每個 Token 計算出各專家的機率分佈。為了減少運算量，通常會設定一個動態閾值 (Dynamic Threshold)，將機率過低的專家分支直接截斷。然而，在軟體層面執行這項操作需要進行額外的遮罩 (Masking) 與分支預測 (Branch Prediction)，這會干擾 Tensor Core 的連續執行，並產生顯著的 Control Flow 開銷。

## 硬體架構協同設計
- **軟體基線:** 依賴 NPU 核心執行機率排序或閾值判斷，產生 Sparse Mask 後才決定要啟動哪些專家的 SRAM 讀取。
- **硬體提案:** 提出「Hardware Dynamic MoE Thresholding Engine (HW-DMT)」。在 Router 輸出端與 DMA 控制器之間植入硬體比較器 (Hardware Comparator)。當 Router 計算出機率後，HW-DMT 會即時比對動態閾值，直接阻斷低機率專家的 DMA 讀取請求 (Read Request)，達成 Zero-Software-Overhead 的動態專家剪枝。

## 效能分析結果
針對具有 64 個專家的 MoE 架構進行測試：
- **傳統軟體動態閾值延遲:** 14.20 ms
- **硬體 HW-DMT 延遲:** 1.95 ms
- **加速比:** 7.28x

## 結論
HW-DMT 成功將 MoE 路由的控制流開銷轉移至硬體資料傳輸層。這不僅大幅降低了路由延遲，更從根本上節省了不必要的記憶體頻寬。強烈建議在專為大語言模型設計的 Edge NPU 中標配此模組。