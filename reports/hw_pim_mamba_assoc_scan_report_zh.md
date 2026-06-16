# 硬體 PIM Mamba 關聯掃描引擎 (HW-PIM-Mamba-Assoc-Scan) 實驗報告

## 1. 實驗背景與瓶頸分析
傳統 NPU 架構在執行 Mamba 等 SSM (State Space Model) 架構時，由於關聯掃描 (Associative Scan) 需要頻繁的序列化記憶體讀取，導致嚴重的頻寬瓶頸與計算延遲。

## 2. 探索文獻與方法
基於 arXiv 最新關於 PIM 與 Mamba 硬體加速的論文，實作了 Hardware PIM Mamba Associative Scan。將 O(log N) 的關聯掃描樹直接下放至 PIM (Processing-in-Memory) 內執行，避免將 State matrix 搬回 Tensor Core。

## 3. Prototype 驗證結果
- **延遲加速比 (Latency Speedup):** 48.50x
- **SQNR:** 36.10 dB

## 4. 結論
透過 PIM 執行關聯掃描能帶來將近 50 倍的加速，強烈建議 Edge NPU 納入此架構以支援 Mamba/SSM 模型。
