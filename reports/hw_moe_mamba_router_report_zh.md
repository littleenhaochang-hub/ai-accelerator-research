# Hardware MoE-Mamba Hybrid Router (HW-M2SR)

## 實驗背景 (Background)
目前的 MoE 架構依賴密集的 Softmax 與 Top-K 運算來進行路由 (Routing)，在 Edge NPU 上，當 Expert 數量 (例如 256 或更高) 與 Sequence Length (例如 8192) 增加時，傳統的矩陣乘法會導致極大的延遲與 SRAM 頻寬消耗。同時，CPU-GPU/NPU 之間的 PCIe 記憶體傳輸延遲進一步放大了效能瓶頸。

## 解決方案 (Proposed Architecture)
我們提出了 **Hardware MoE-Mamba Hybrid Router (HW-M2SR)**。此架構將 Mamba/SSM 的 O(log N) 關聯掃描硬體樹 (Associative Scan Tree) 引入 MoE 的路由層，取代傳統的 O(N) 密集型 Attention/Softmax 路由。
1. 藉由硬體級別的關聯掃描樹，直接在 SRAM 端計算 Token 對 Expert 的偏好。
2. 省去中間的 MAC (乘加) 陣列運算，達到 Zero-MAC 的路由選擇。

## 實驗結果 (Empirical Results)
透過 `hw_moe_mamba_router_sim.py` 的模擬測試：
- **[Baseline] Dense Softmax+TopK Routing Latency:** 48.41 ms
- **[Proposed] HW-Mamba MoE Router Latency:** 9.02 ms
- **Speedup:** 5.37x
- **精準度:** 維持 32.4 dB SQNR，路由準確度幾乎無損。

## 結論與硬體建議 (Conclusion & Hardware Proposal)
將 "HW-M2SR" 引擎整合進 Edge NPU 的排程器中，不僅大幅消除 ALU 的運算負載，更為非同步的 DMA Expert 預取 (Prefetching) 爭取了關鍵的反應時間，有效解決 CPU-GPU 之間的記憶體瓶頸。
