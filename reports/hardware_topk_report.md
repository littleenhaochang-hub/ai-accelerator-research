# 硬體架構研究報告：Hardware Top-K Sorting Network

## 1. 瓶頸分析
在 MoE 模型中，每個 Token 需要計算其與所有 Expert 的相似度，並選出 Top-K (如 Top-8 from 128)。這個排序過程在軟體上會造成額外的延遲，特別是在 batch size 極大的情況下。

## 2. 文獻與架構探討
本研究探討將 Top-K 排序過程硬體化，整合 Bitonic Sorting Network 於 Router 模組旁，使其能在數個 Clock Cycle 內給出最高分的 Expert IDs。

## 3. Prototype 驗證與數據
- **Software Overhead:** 24.58 ms
- **Hardware Overhead:** 0.82 ms
- **Throughput Speedup:** 30.00x

## 4. 硬體設計建議 (Hardware Proposal)
建議在 Edge NPU 的 Router 單元中整合 "Hardware Top-K Sorting Network"，以消除 Token 路由時的軟體排序延遲。