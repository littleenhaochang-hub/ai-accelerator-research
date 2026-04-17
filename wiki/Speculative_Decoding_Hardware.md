# Speculative Decoding: Asymmetric Dual-Engine Execution

## 實驗背景
自回歸解碼受限於記憶體頻寬 (Memory-Bound)。Speculative Decoding 透過小模型 (Draft) 預測、大模型 (Target) 驗證，將 Sequential 過程部分轉換為 Parallel 過程。

## 模擬結果
- **腳本**: `speculative_decoding_sim.py`
- 模擬在 Acceptance Rate 70%、Gamma=4 情況下，可獲得約 **1.51x ~ 2.0x** 的推論加速。

## 硬體架構協同設計
Edge NPU 應採用「**非對稱雙引擎 (Asymmetric Dual-Engine)**」架構：
1. **Draft Engine**: 具備極低延遲的 Scalar/Vector 運算單元，參數完全駐留於 SRAM (如 W4A4 or Sub-2-bit)，專注於高速自回歸。
2. **Target Engine**: 高吞吐量的 Matrix/Tensor 核心，從 LPDDR/Unified Memory 串流載入權重，對 Draft 的輸出進行大批次平行驗證。
藉由分離計算引擎，消除 Draft 與 Target 之間的資源競爭。
