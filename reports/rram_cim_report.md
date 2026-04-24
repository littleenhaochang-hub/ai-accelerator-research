# RRAM 記憶體內運算 (Compute-in-Memory) 架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
將百億參數的 LLM 部署到邊緣裝置 (Edge NPU) 時，最大的挑戰之一是 SRAM 的靜態漏電功耗 (Static Leakage Power)。以一個 7B 模型 (INT4 量化，約 3.5GB) 為例，若全部塞入 SRAM 中，光是維持資料不流失的靜態漏電就高達將近 8.75 瓦特，這對於靠電池供電的穿戴裝置或手機來說是不可接受的。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
我們提出了基於 **RRAM (Resistive RAM, 阻變式記憶體)** 的記憶體內運算 (Compute-in-Memory, CIM) 架構。RRAM 具有非揮發性 (Non-volatile) 特質，不僅能將靜態漏電降至趨近於零，更能直接利用記憶體交叉陣列 (Crossbar Array) 的物理定律 (歐姆定律與基爾霍夫電流定律) 在類比域完成矩陣乘加 (MAC) 運算。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`rram_cim_sim.py`
- **SRAM 漏電功耗**: 8750.00 mW (8.75W)
- **RRAM 漏電功耗**: 35.00 mW (0.035W)
- **靜態功耗降低 (Static Power Reduction)**: **250.00x**
- **動態運算能耗降低 (Dynamic Energy Reduction)**: **5.00x**

## 4. 硬體架構建議
針對次世代無電池或超低功耗物聯網 (IoT) 邊緣裝置，強烈建議捨棄傳統的大容量 SRAM 設計，轉向採用 RRAM CIM 架構。將 LLM 的靜態權重直接燒錄進 RRAM 陣列中，不僅能徹底消滅漏電功耗牆，還能透過類比運算大幅提升動態能效比 (TOPS/W)。
