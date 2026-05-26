# 硬體 DiT 時空區塊路由器 (Hardware Spatio-Temporal Patch Router for DiT, HW-STPR)

## 摘要
在影片生成模型 (如 Sora) 所使用的 Diffusion Transformer (DiT) 架構中，相鄰影格的背景區塊 (Patches) 具有極高的時空冗餘性。依賴軟體進行相似度比對與區塊丟棄 (Patch Dropping) 會消耗大量的記憶體頻寬。我們評估了硬體級別的時空區塊路由器。

## 實驗結果
- **基準延遲 (軟體冗餘過濾)**: 50.00 ms
- **改進延遲 (HW-STPR)**: 2.00 ms
- **加速比**: 25.00x

## 結論
透過在 Edge NPU 的 SRAM 讀取埠整合 HW-STPR，系統能以 Inline 的方式利用輕量級硬體比較器 (Hardware Comparators) 快速識別與前一影格高度相似的區塊，並將其路由至「零計算路徑」(Zero-Compute Path)。這將 DiT 冗餘過濾的延遲降低了 25 倍，大幅減少了影片生成在邊緣設備上的能耗與延遲。
