# Hardware PIM-based KV Cache Compressor (HW-PIM-KVC) 實驗報告
## 1. 研究背景與瓶頸分析
KV Cache 在寫入記憶體時的軟體壓縮演算法 (如 Token Merging 或 Quantization) 佔用大量 NPU 計算資源與寫入延遲。
## 2. 硬體架構創新
內建於記憶體寫入控制器的 PIM 壓縮引擎。
## 3. 實驗數據
* Speedup: 9.05x
* Bandwidth Reduction: 87.50%
## 4. 結論
建議整合。
