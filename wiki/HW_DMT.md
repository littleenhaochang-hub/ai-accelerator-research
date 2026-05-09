# Hardware Dynamic MoE Thresholding Engine (HW-DMT)

## 實驗背景
大規模 MoE 模型的軟體 Top-K 排序與遮蔽造成嚴重的控制流負載，拖慢路由速度。

## 架構設計
透過硬體並行比較器，在 Logits 輸出後立即剔除低機率專家，阻斷無效的 DMA 讀取請求。

## 模擬結果
*   **基準:** 12.80 ms (8K context, 256 experts)
*   **HW-DMT:** 1.60 ms
*   **總結提升:** 8.00x 路由加速。

建議將此設計列入 Edge NPU 路由器規格，消除 MoE 軟體排序瓶頸。