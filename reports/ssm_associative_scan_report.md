# SSM/Mamba Associative Scan 硬體架構研究報告

## 背景與瓶頸分析
根據 `RESEARCH_REPORT.md`，SSM (State Space Models) 如 Mamba 在推論和訓練時的狀態更新具有循序相依性 (Sequential Dependency)，導致 O(N) 的計算瓶頸，無法充分利用現代 NPU/GPU 龐大的平行計算資源。

## 解決方案：硬體層級的平行前綴和關聯掃描 (Associative Parallel Prefix Scan)
我們設計了專用的硬體關聯掃描樹 (Associative Scan ALU Tree)，將 O(N) 的循序相依性轉換為 O(log N) 的樹狀深度計算。透過增加專用的加法與乘法 ALU 樹，可以在硬體層次直接平行處理 SSM 的狀態更新。

## 實驗結果
透過 Python 原型 `ssm_associative_scan_sim.py` 進行模擬：
- **測試環境：** 序列長度 8192，ALU 延遲 2.0 ns，256 個 ALU。
- **傳統循序計算延遲：** 16384.00 ns
- **平行掃描樹延遲：** 26.00 ns
- **加速比 (Speedup)：** 630.15x

## 結論與架構建議
實驗證明，將 SSM 的掃描過程硬體化能帶來數百倍的延遲縮減。
**硬體架構建議：** 建議在 Edge NPU 的設計中加入「專用關聯掃描 ALU 樹 (Associative Scan ALU Trees)」，以支援 Mamba/SSM 類模型的原生硬體加速。
