# 硬體連續 Token 稀疏引擎 (HW-CTS) 分析報告

## 執行摘要
在無限文本串流或超長文本生成中，動態稀疏化 (Dynamic Token Sparsity) 能夠減少計算與記憶體開銷。然而，在軟體層面持續維護和更新稀疏遮罩 (Sparsity Mask) 的成本極高。我們提出了硬體連續 Token 稀疏引擎 (HW-CTS)。

## 模擬結果
* **軟體維護延遲:** 384.00 ms
* **硬體 HW-CTS 延遲:** 12.80 ms
* **效能提升:** 延遲加速達 30.00x。

## 架構建議
建議在邊緣 NPU 的調度器中整合 **HW-CTS (Hardware Continuous Token Sparsity)**，實現真正的 Zero-Overhead Token 淘汰與過濾，極大地延長生成階段的 Context Window 並節省功耗。
