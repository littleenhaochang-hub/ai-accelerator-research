# Hardware Accelerated Prompt Caching (HW-APC)

## 實驗背景 (Background)
在 Agentic AI 工作流中，系統經常需要重複處理龐大的 System Prompt (如 64K+ 的系統指令)。軟體的 Prefix Caching (如 Radix Tree) 存在顯著的 CPU 查找延遲。

## 實驗設計 (Methodology)
本實驗設計了整合 TCAM (Ternary Content-Addressable Memory) 的硬體級 Prompt 快取引擎 (`hw_apc_sim.py`)。將 Prefix Token 的 Hash 直接存入 TCAM，實現 $O(1)$ 的硬體級查表與 SRAM 直接映射。

## 實驗結果 (Results)
- Software Prefix Caching: 0.0151 s
- HW-APC TCAM Latency: 0.0005 s
- **Speedup**: 29.49x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 內建「HW-APC TCAM 引擎」，專門用於 Multi-Agent 場景下的高頻率 System Prompt 快取。這能完全消除 CPU 介入的延遲，大幅提升 Agent 反應速度。