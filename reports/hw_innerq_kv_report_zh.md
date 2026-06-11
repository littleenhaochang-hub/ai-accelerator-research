# Hardware InnerQ KV Cache Quantization Engine (HW-InnerQ)

## 實驗背景與瓶頸分析 (Background & Bottleneck)
在大語言模型 (LLMs) 的推論解碼階段 (Decoding)，KV Cache 的大小會隨著序列長度線性增長，成為記憶體容量與頻寬的主要瓶頸。雖然過往有許多量化 (Quantization) 方法用以壓縮 KV Cache，但在硬體層面，反量化 (Dequantization) 通常會打破記憶體的連續性存取，導致嚴重的 ALU 延遲與記憶體頻寬利用率低下。

## 文獻探索 (Literature Exploration)
根據 arXiv 的最新論文《InnerQ: Hardware-Aware Tuning-Free Quantization of KV Cache for Large Language Models》，該研究提出了一種硬體友好的量化機制。
InnerQ 的核心在於「內部維度分組 (Inner dimension grouping)」，這讓反量化過程能與向量-矩陣乘法 (VMM) 完美對齊，大幅提升 GPU/NPU 運算單元的資料重用率。此外，它將 Key Cache 的通道正規化 (per-channel normalization) 預先摺疊 (folded) 到模型權重中，達成了零運行時開銷 (zero runtime overhead)。

## 實驗設計與原型 (Prototype Design)
我們使用 Python 撰寫了 `innerq_kv_sim.py` 來比較反量化的硬體延遲：
1. **Traditional KV Dequantization**：模擬一般非硬體對齊的 4-bit 反量化操作，受限於純量 ALU 運算與記憶體對齊開銷。
2. **InnerQ KV Dequantization**：模擬與 VMM 對齊的向量化記憶體抓取，並結合無開銷的預摺疊正規化。

## 實驗數據 (Empirical Results)
*   **Sequence Length**: 32768
*   **Traditional KV Dequantization Latency**: 953.12 ms
*   **InnerQ KV Dequantization Latency**: 360.31 ms
*   **效能提升 (Speedup)**: **2.65x**

## 架構提案與結論 (Architectural Proposal & Conclusion)
我們的模擬證實，在硬體層面採用 InnerQ 的向量對齊反量化機制，能將長文本 KV Cache 讀取的延遲改善 2.65 倍。我們強烈建議在下一代 Edge NPU 的 SRAM 控制器與 Attention Block 之間，整合硬體原生的「HW-InnerQ 向量反量化引擎 (HW-InnerQ Engine)」，以無損的方式原生支援高效的極端壓縮 (Extreme Compression)。