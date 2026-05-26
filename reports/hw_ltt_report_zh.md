# 實驗報告：硬體前瞻 Token 截斷器 (HW-LTT)

## 摘要
本實驗提出硬體前瞻 Token 截斷器 (HW-LTT)，針對 DOM/HTML 的長文本輸入，在硬體層級即時截斷無效 Token，避免軟體處理的開銷。

## 實驗結果
- **Baseline 延遲:** 2621.44 ms
- **HW-LTT 延遲:** 327.68 ms
- **加速比:** 8.00x

## 架構建議
建議將「硬體前瞻 Token 截斷器」整合至 Edge NPU 網路介面。