# Hardware Asynchronous Tensor-Parallel Interconnect (HW-ATPI)

## 實驗背景 (Background)
為了在 Edge 端執行超過 30B 以上的大模型，單一 NPU 的 SRAM 往往不足，需要採用 Multi-Chiplet 進行 Tensor Parallelism。然而，傳統由 CPU 主導的 PCIe All-Reduce 會帶來極大的同步延遲。

## 實驗設計 (Methodology)
本實驗設計了專用的硬體非同步張量平行互連架構 (`hw_atpi_sim.py`)。透過 Die-to-Die (D2D) 的專用硬體通道，HW-ATPI 允許不同 Chiplet 的 Tensor Core 直接在硬體層面進行 All-Reduce 運算，完全繞過 CPU 與 PCIe 驅動程式。

## 實驗結果 (Results)
- Software All-Reduce Latency: 0.0114 s
- HW-ATPI Interconnect Latency: 0.0035 s
- **Speedup**: 3.29x

## 硬體提案 (Hardware Proposal)
建議在下一代 Multi-Chiplet Edge NPU 中導入「HW-ATPI 互連網路」，使多個 NPU Die 在邏輯上完全融合成單一處理器，消除張量平行運算時的通訊牆。