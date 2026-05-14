# Hardware System-2 Search Controller (HW-S2SC)

## 實驗背景 (Background)
在具備 System 2 (Test-Time Compute) 的推理模型 (如類似 o1 的架構) 中，需要進行大量的 Monte Carlo Tree Search (MCTS) 或是多路徑探索。傳統作法依賴 CPU 與 NPU 頻繁同步，產生極大的 PCIe 通訊與排程延遲。

## 實驗設計 (Methodology)
本實驗設計了硬體級別的搜索控制器 (`hw_sys2_search_sim.py`)。透過將 MCTS 樹狀結構的管理與節點擴展 (Node Expansion) 邏輯直接下放至 NPU 內建的 SRAM 控制器，消除 CPU-GPU 同步瓶頸。

## 實驗結果 (Results)
- Software MCTS Search Latency (512 nodes): 2.5600 s
- HW-S2SC Latency: 0.0512 s
- **Speedup**: 50.00x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 內建「HW-S2SC 樹狀搜索控制器」，專為下一代具備 System-2 Test-Time Compute 的推理模型設計，實現在硬體底層的無縫節點擴展與評估。