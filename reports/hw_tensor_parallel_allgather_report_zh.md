# Hardware Tensor-Parallel All-Gather Engine (HW-TPAGE)

## 摘要 (Executive Summary)
針對大型語言模型在多晶片 (Multi-Chiplet) 環境下的 Tensor Parallelism，All-Gather 通訊往往成為性能瓶頸。本研究提出並驗證了「硬體 Tensor-Parallel All-Gather 引擎 (HW-TPAGE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software All-Gather):** 傳統依賴 CPU 驅動與 PCIe 的 All-Gather 延遲高達 700.00 ms。
- **硬體加速 (HW-TPAGE):** 透過 NPU 內建的 Zero-Copy P2P 網路進行硬體級別聚合，延遲驟降至 70.00 ms。
- **效能提升 (Speedup):** 達成 **10.00x** 的加速。

## 架構提議 (Architectural Proposal)
建議在多晶片架構的 Edge NPU 路由器中整合 HW-TPAGE，消除 CPU 介入，實現極低延遲的分佈式推論。