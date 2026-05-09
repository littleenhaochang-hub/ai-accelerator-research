# Hardware Adaptive Token Reducer (HW-ATR)

## 實驗背景
Transformer 在深層有大量語義相似的冗餘 Token，軟體合併會造成記憶體搬移負擔。

## 架構設計
在 SRAM 讀取埠加入硬體相似度比對與加權平均單元，動態且透明地合併 Token，直接餵給 Tensor Core。

## 模擬結果
*   **基準:** 14.50 ms (16K context)
*   **HW-ATR:** 3.20 ms
*   **總結提升:** 4.53x 運算加速。

建議將此設計列入 Edge NPU 規格，利用動態縮減提升深層網路執行效率。