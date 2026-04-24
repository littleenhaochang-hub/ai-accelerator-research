# Liquid Neural Networks (LNN) ODE 硬體求解器架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
Liquid Neural Networks (LNN) 在處理時序資料與邊緣自適應任務時表現優異，但其神經元狀態依賴常微分方程 (Ordinary Differential Equations, ODEs) 的連續時間推演。傳統的 Edge NPU 專為稠密矩陣乘法 (MAC) 設計，若以軟體 (如 Euler method) 計算 ODE，會牽涉大量效率極低的純量運算、除法與指數函數 (EXP)，導致推論延遲大幅增加。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
為了解決此問題，我們提出在 NPU 內部整合專用的 **Hardware ODE Solver (硬體常微分方程求解器)**。該單元採用 Piecewise Linear (PWL) 近似法與硬體查表 (LUT)，將複雜的 ODE 狀態更新融合成單一硬體管線，使用定點數 (Fixed-point) 運算在每個時鐘週期完成神經元狀態迭代。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`lnn_ode_hardware_sim.py`
- **數位 MAC 陣列 (軟體 Euler)**: 推論延遲 12288.00 us
- **硬體 ODE 求解器**: 推論延遲 2048.00 us
- **運算加速 (Speedup)**: **6.00x**

## 4. 硬體架構建議
對於未來的機器人控制晶片或自駕車 Edge NPU，強烈建議在標準 Tensor Core 旁配置 Dedicated Hardware ODE Solver。這不僅能釋放主算力單元的壓力，還能將 LNN 這種具備高度時序適應性的連續時間模型延遲縮減 6 倍，滿足毫秒級的即時控制需求。
