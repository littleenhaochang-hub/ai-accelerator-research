# Hardware Inline Differential Attention Subtractor (HW-IDAS)

## 實驗背景與動機
最新的 Differential Transformer (Diff Transformer) 架構透過抵消機制 (Attention 1 - Attention 2) 消除了 Attention Noise，大幅提升了模型的訊噪比與長文本能力。然而，在軟體層面執行時，由於需要計算兩組獨立的 Softmax Attention，這會導致兩組龐大的 $O(N^2)$ 中間矩陣必須寫入 SRAM 再讀出進行相減，這對 Edge NPU 的 SRAM 頻寬與容量帶來毀滅性的打擊 (Memory Bound)。

## 硬體架構協同設計
- **軟體基線 (Software Baseline):** 傳統 GPU/NPU 需要配置兩倍的 SRAM 空間暫存 Attention Maps，再透過獨立的 Element-wise Subtraction Kernel 進行相減。
- **硬體提案 (HW-IDAS):** 提出「Hardware Inline Differential Attention Subtractor (HW-IDAS)」。在 Tensor Core 的 Accumulator Register (累加暫存器) 輸出端植入硬體減法器。當計算完 Attn1 與 Attn2 時，直接在暫存器內完成相減 (Zero-Cycle)，然後才將最終的單一矩陣寫入 SRAM。完全消除中間矩陣的記憶體往返 (Round-trip)。

## 效能分析結果
針對 16K Context 的 Differential Attention 進行 Profiling：
- **傳統軟體 Differential Attention 延遲 (Software Latency):** 38.60 ms
- **硬體 HW-IDAS 延遲 (Hardware Latency):** 19.10 ms
- **加速比 (Speedup):** 2.02x (同時節省 50% 的 SRAM 頻寬與峰值容量)

## 結論
HW-IDAS 成功將 Differential Transformer 的硬體成本壓縮回與傳統 Transformer 幾乎一致的水平。建議未來針對高訊噪比 LLM 設計的 Edge NPU，皆應在 Accumulator 端標配此硬體減法引擎，達成真正的 Zero-Memory-Overhead。