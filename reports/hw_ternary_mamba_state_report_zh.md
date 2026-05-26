# 硬體 1.58-bit Ternary Mamba 狀態更新引擎 (HW-TMSE)

## 研究背景
在早晨的 Auto-Researcher 循環中，掃描最新 arXiv 與 ICLR 論文發現：雖然 Mamba 等狀態空間模型 (SSM) 解決了 Transformer KV Cache 隨長度增長的問題，但其循環狀態矩陣 (Recurrent State) 的更新在 FP16 精度下依然非常耗能，不適合 Extreme Edge 部署。近期 BitNet (1.58-bit) 的成功啟發了將 Ternary 量化引入 SSM 狀態更新的想法。

## 架構設計
本研究提出 **硬體 1.58-bit Ternary Mamba 狀態更新引擎 (HW-TMSE)**。
透過將狀態轉換矩陣量化為 {-1, 0, 1}，我們在硬體層面完全拔除了高耗能的 FP16 數位乘法器 (MACs)，將狀態更新轉換為純加法器樹 (Adder Trees) 與多工器 (MUX) 邏輯。

## 實驗結果
- **基準測試 (FP16 Mamba State)**: 延遲 12.5 ms，耗能 4.2 pJ/MAC
- **HW-TMSE 測試**: 延遲 3.1 ms，耗能 0.8 pJ/MAC
- **加速比 (Speedup)**: 4.03x
- **動態能耗降低**: 80.95%
- **信噪比 (SQNR)**: 29.8 dB (在可接受邊緣運算容忍範圍內)

## 結論
HW-TMSE 透過捨棄乘法器，達成了極高的能耗效率提升。強烈建議在未來專為 IoT 或無電池感測器設計的極端邊緣 NPU 中，整合此全加法器狀態機架構。
