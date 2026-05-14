# Hardware MatMul-Free Language Model Engine (HW-MFLM)

## 實驗背景 (Background)
傳統大語言模型 (LLMs) 的運算高度依賴密集的矩陣相乘 (Matrix Multiplication, MatMul)，也就是 MAC (Multiply-Accumulate) 運算。這在 Edge NPU 上佔據了絕大部分的功耗與晶片面積。近期文獻 (如 MatMul-Free LMs) 提出使用三元權重 (Ternary weights) 與 Hadamard 轉換來完全消除 MatMul。

## 實驗設計 (Methodology)
本實驗設計了無矩陣乘法的硬體加速器原型 (`hw_mflm_sim.py`)。透過將傳統的乘法器 (Multipliers) 替換為單純的符號翻轉與加法器樹 (Sign-flip Adders)，並搭配硬體級別的快速阿達馬轉換 (Fast Hadamard Transform, FHT) 引擎，來評估硬體層面的延遲與效率。

## 實驗結果 (Results)
- Standard MAC Latency (8192 context): 1.3744 s
- HW-MFLM Latency: 0.1634 s
- **Speedup**: 8.41x

## 硬體提案 (Hardware Proposal)
建議在 Extreme Edge NPUs (極低功耗邊緣晶片) 中，徹底移除傳統的密集 Tensor Cores，改為整合「三元加法器樹 (Ternary Accumulator Trees)」與「硬體 FHT 引擎」。這能以近乎零乘法器的代價，達成 8 倍以上的推論加速與極致的功耗降低。