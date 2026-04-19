# MoE Expert Ring Interconnect 硬體架構研究報告

## 背景與瓶頸分析
根據先前的實驗與 `RESEARCH_REPORT.md`，MoE (Mixture of Experts) 在推論 (Decoding) 階段會遭遇嚴重的 CPU-GPU 或 DRAM-NPU 記憶體傳輸瓶頸。當多個 NPU 同時需要從主記憶體或 CPU 提取不同的 Expert 權重時，傳統的 Hub-and-Spoke (星型/集線器) 拓撲會導致 PCIe 或主記憶體頻寬雍塞，造成嚴重的延遲。

## 解決方案：硬體級 MoE 專家環狀網路 (MoE Expert Ring Interconnect)
我們參考了 Ring Attention 的概念，將其應用於 MoE 的硬體傳輸上。我們設計了一套 P2P (Peer-to-Peer) 的環狀互連架構，讓 Expert 權重在 NPU 之間以管線化 (Pipelined) 的方式傳遞。各個 NPU 只需要在所需的 Expert 經過自己時將其載入 SRAM，大幅降低了中心節點的頻寬壓力。

## 實驗結果
透過 Python 原型 `moe_ring_expert_sim.py` 進行循環精確度模擬：
- **測試環境：** 8 個 NPU，單一 Expert 大小 2.0GB，環狀頻寬 100GB/s，單步延遲 0.5ms。
- **傳統 Hub-and-Spoke 傳輸時間：** 160.00 ms
- **Ring Interconnect 傳輸時間：** 82.00 ms
- **加速比 (Speedup)：** 1.95x

## 結論與架構建議
實驗證明，MoE Expert Ring Interconnect 能有效緩解 PCIe/CPU 的 MoE 傳輸瓶頸。
**硬體架構建議：** 在未來的 Multi-Chiplet 或 Edge NPU 集群設計中，應整合「專用 MoE 環狀 DMA 控制器 (MoE Ring DMA Controller)」，支援硬體層級的權重循環傳遞機制，使推論過程能保持 Compute-bound。
