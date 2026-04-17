# Auto-Researcher 實驗報告：Ring Attention 與 Context Parallelism
**日期:** 2026-04-13

## 1. 瓶頸分析
根據 `RESEARCH_REPORT.md`，處理百萬級別 Token (Million-Token Contexts) 的 LLM 推論時，單一 NPU/GPU 的 VRAM 無法容納完整的 KV Cache。強制儲存會導致 OOM，若放回 CPU DRAM 則受限於 PCIe 頻寬造成嚴重卡頓。

## 2. 文獻探索
透過檢索 arXiv 2025/2026, ICLR 2026 論文 (如 "Out of the Memory Barrier", "Star Attention")，我們發現：
*   **Ring Attention:** 將超長 Context 均分給多個硬體節點 (Context Parallelism)。每個節點只存放自己負責的 KV Block，並透過 Peer-to-Peer Ring 通訊，輪流將 KV Block 傳遞給相鄰節點進行注意力計算。
*   此方法大幅降低了峰值記憶體需求，且免去了全域同步 (Global Synchronization) 的開銷。

## 3. Prototype 驗證
我們在 `ring_attention_prototype.py` 模擬了 4 顆 NPU 的 Ring Bus 架構，總 Token 數高達 131K：
*   每顆 NPU 只需負擔 32K Token 的 KV 記憶體 (約 0.5 GB per layer)。
*   假設 Ring Bus 頻寬為 100 GB/s，每一步 KV 區塊傳遞僅需 5.0 ms。
*   總通訊延遲僅 15.0 ms，且可完美與矩陣計算 (Compute) 進行非同步重疊 (Overlap)。

## 4. 結論
針對超長文本處理的硬體架構，我們的 Accelerator Network-on-Chip (NoC) 必須支援 **P2P Ring Topology DMA**，讓 NPU 之間能直接交換 SRAM/DRAM 中的 KV Cache，無需 CPU 介入。這能實現真正「無限長度」的 Context Parallelism 推論。此結論已紀錄。
