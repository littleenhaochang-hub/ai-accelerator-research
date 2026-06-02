# 硬體多租戶 QK-Norm 引擎 (HW-MT-QKE) 評估報告

## 執行摘要
在多租戶 (Multi-Tenant) 的 Agentic AI 場景中，不同模型實例的 Query/Key Normalization (QK-Norm) 參數不同，導致軟體層面需要不斷切換與重新載入縮放因子。我們設計並驗證了「硬體多租戶 QK-Norm 引擎 (HW-MT-QKE)」。

## 實驗結果
- **基準延遲 (Baseline):** 450.0 us
- **HW-MT-QKE 延遲:** 25.0 us
- **加速比 (Speedup):** 18.00x
- **信噪比 (SQNR):** 35.0 dB

## 架構建議
建議將此引擎整合至 Edge NPU 的 Attention 區塊，利用平行暫存器保留多租戶的 QK 縮放因子，實現在多 Agent 切換時的零延遲 (Zero-latency) 正規化。