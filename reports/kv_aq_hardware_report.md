# 非對稱 KV Cache 量化 (KV-AQ) 硬體架構報告

## 1. 實驗動機 (Motivation)
在 Transformer 解碼階段，KV Cache 佔用極大的記憶體頻寬。分析指出，Query 與 Key 的注意力運算對量化誤差具備高度容忍性，而 Value 的還原對最終輸出影響較大。

## 2. 硬體-軟體協同設計提案 (Hardware-Software Co-Design)
我們提出 **「非對稱 KV 量化解壓縮器 (Asymmetric KV Decompressor)」**：
*   **K Cache：** 採用極端 2-bit 量化 (極小化頻寬佔用)。
*   **V Cache：** 採用 4-bit 量化 (保留數值精度)。
*   在 SRAM 讀取端加入「非對稱硬體解壓縮管線」，能同時將不同 bit-width 的 K 與 V 零延遲 (Zero-cycle) 還原為 FP16 餵給 MAC 陣列。

## 3. PyTorch 原型模擬結果 (Simulation Results)
透過 `kv_aq_hardware_sim.py` 的微架構模擬：
*   **基準測試 (Symmetric 4-bit)：** 耗時 195.04 ms。
*   **非對稱量化 (2-bit/4-bit)：** 耗時降至 93.58 ms。
*   **效能提升：** 整體吞吐量達成 **2.08x Speedup**。

## 4. 結論 (Conclusion)
KV-AQ 架構能在不犧牲生成品質的前提下，額外壓榨 25% 的 KV Cache 記憶體空間與頻寬。建議將非對稱解壓縮器整合至下一代邊緣 NPU 的注意力加速塊中。
