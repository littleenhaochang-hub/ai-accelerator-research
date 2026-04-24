# Hardware GEMV (Vector-MAC) Engine (硬體解碼專用向量矩陣引擎)

## 實驗背景 (Background)
目前的 Edge NPU 主要採用 2D 脈動陣列 (Systolic Array) 來加速矩陣相乘 (GEMM)，這在長文本輸入的 Prefill 階段非常高效。然而，在 Token 逐字生成的 Decode 階段 (Batch=1)，運算退化為矩陣-向量相乘 (GEMV)。若將單一向量餵入龐大的 2D 陣列，會導致運算單元利用率低於 5%，這是目前 Edge 設備生成速度 (TPS) 緩慢的最大硬體死穴。

## 物理模擬 (Physical Simulation)
透過 `gemv_decode_hw_sim.py`，我們模擬了使用傳統 2D 脈動陣列與專用 1D Vector-MAC (VMAC) 引擎進行 Decode 的效能：
- **傳統脈動陣列延遲 (2048 Tokens)**: 16777.22 ms
- **專用 VMAC 引擎延遲**: 838.86 ms
- **整體加速比**: 20.00x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 中導入 **「Heterogeneous Prefill-Decode (異質推論)」** 架構。
在原有的 2D 脈動陣列旁，並行建置專為 GEMV 設計的 **「1D Vector-MAC (VMAC) Engine」**，並將其緊貼 SRAM 記憶體庫。在 Prefill 階段，資料走 2D 陣列；進入 Decode 階段後，硬體自動將資料流切換至 1D VMAC 引擎。這能達成 100% 的運算利用率，為本地 Agentic AI 帶來突破性的流暢生成體驗。
