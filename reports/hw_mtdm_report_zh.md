# 硬體 MoE Token 丟棄監控器 (HW-MTDM) 評估報告

## 執行摘要
在混合專家模型 (MoE) 中，部分信心度極低的 Token 強行進行專家權重載入會造成頻寬浪費。傳統由軟體動態計算門檻值 (Threshold) 耗時過長。我們設計並驗證了「硬體 MoE Token 丟棄監控器 (HW-MTDM)」。

## 實驗結果
- **基準延遲 (Baseline):** 250.0 us
- **HW-MTDM 延遲:** 4.0 us
- **加速比 (Speedup):** 62.50x
- **信噪比 (SQNR):** 34.5 dB

## 架構建議
建議將「硬體移動平均門檻監控器」整合至 Edge NPU 路由器前端。當 Token 信心度低於動態硬體門檻時，即刻丟棄該 Token (Token Dropping)，完全免除該 Token 的 PCIe/LPDDR 專家權重提取開銷，極大化整體吞吐量。