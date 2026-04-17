# Ring Attention Multi-Chiplet Architecture

## 實驗背景
為了處理 32K+ 甚至無限長度的 Context，單一 NPU 的 SRAM 絕對無法容納完整的 KV Cache。Ring Attention 將 KV Cache 切塊分佈在多個 NPU Chiplet 之間，並利用 Ring Topology 輪轉傳輸。

## 硬體模擬與分析
- **腳本**: `ring_attention_sim.py`
- 模擬 4 個 Chiplets 處理 32K Context，Block Compute 耗時 0.859 ms，Inter-Chiplet 傳輸耗時 0.021 ms。
- 透過 Async Overlap，完全隱藏了傳輸延遲，保證系統處於 100% Compute Bound。

## 架構協同設計結論
Edge NPU 若要朝向 Scalable Architecture 發展，封裝上應採用 Multi-Chiplet 且具備 **D2D (Die-to-Die) Ring Interconnect** 網路層。NPU 內的 DMA 引擎必須支援硬體層級的 Token Ring 輪轉廣播，與 MAC Array 的運算完美解耦。
