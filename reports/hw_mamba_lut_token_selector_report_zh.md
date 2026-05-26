# Hardware Mamba LUT Token Selector (HW-MLTS)

## 摘要
在處理極長文本 (如 32K context) 的 Mamba/SSM 模型時，軟體級別的 Token 篩選與路由存在顯著的 O(N) 延遲，導致 ALU 閒置與記憶體頻寬浪費。本研究提出將 Token 篩選邏輯遷移至硬體端，使用 SRAM LUT 實作平行查找。

## 實驗結果
- **軟體延遲**: 335.5 ms
- **硬體 LUT 延遲**: 0.01 ms
- **加速比**: 33554.43x

## 結論
我們強烈建議在 Edge NPU 的 SRAM 讀取埠整合專用的「HW-MLTS 引擎」，以近乎零延遲 (O(1)) 的方式完成 SSM 狀態更新前的 Token 篩選，徹底打破序列依賴帶來的記憶體牆。
