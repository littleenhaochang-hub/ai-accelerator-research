# Edge Agentic AI: BPE Tokenizer 硬體加速器架構研究

## 1. 瓶頸分析 (Bottleneck Analysis)
在邊緣裝置 (如 Mac mini 或穿戴設備) 執行 Agentic AI 時，必須處理大量的 HTML DOM 與系統日誌。我們發現，在將 32K Token 的字元傳入模型前，CPU 負責的 BPE (Byte-Pair Encoding) Tokenization 會產生嚴重的延遲。這是因為軟體實作依賴雜湊表與字串比對，導致大量的快取未命中 (Cache misses) 與分支預測失敗 (Branch mispredictions)。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
為了消除 Prefill 前的 CPU 瓶頸，我們設計了 **Hardware BPE Tokenizer (硬體 BPE 分詞器)**。該架構將 BPE 字典編譯為硬體 Trie-Tree (前綴樹) 結構，並實作一個「硬體狀態機 (Hardware Trie-Walker)」直接部署於 NPU SRAM 旁。它能以接近 Zero-branch penalty 的方式，用有限狀態機在每個時鐘週期平行走訪字串。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`hw_bpe_tokenizer_sim.py`
- **CPU 軟體分詞 (3GHz)**: 處理 100K 字元約需 5.00 ms
- **NPU 硬體分詞 (1GHz)**: 處理 100K 字元僅需 0.30 ms
- **運算加速 (Speedup)**: **16.67x**

## 4. 硬體架構建議
對於未來專注於 Agentic AI 的晶片架構，Tokenization 不應再留給 CPU。強烈建議在 NPU 前端整合「Hardware Trie-Walker 引擎」，讓原始字串能以 DMA 方式直通硬體分詞器，隨後無縫銜接至張量核心進行 Prefill，徹底實現 End-to-End 硬體加速。
