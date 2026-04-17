# BitNet 1.58-bit (Ternary) Hardware Architecture

## 實驗背景
為了將模型推論極限推向次 2-bit 領域 (Sub-2-bit Quantization)，我們探討 BitNet b1.58 權重 `{-1, 0, 1}` 在硬體上的真實能效。這項技術的本質是將矩陣乘加 (MAC) 降維為單純的累加與減法。

## 硬體模擬與分析
- **腳本**: `bitnet_hardware_sim.py`
- 與傳統 INT8 MAC (0.2 pJ) 相比，INT Add (0.05 pJ) 的基礎能效已有 4x 提升。
- 若結合三元權重自然產生的稀疏性 (~20% 的 0)，引入 Zero-Skipping 後，總能效提升高達 **5.00x**。

## 架構協同設計結論
Edge NPU 藍圖中，應加入 **Ternary ALU Arrays (純加減法器陣列)**。移除乘法器能省下極大的晶片面積 (Area)，騰出的空間可用來加大 SRAM，進一步緩解 Memory Wall 的問題。
