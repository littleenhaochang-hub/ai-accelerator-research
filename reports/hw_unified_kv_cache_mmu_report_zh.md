# Auto-Researcher 分析報告：Hardware Unified KV Cache MMU (HUKV-MMU)

## 實驗背景
在多代理 (Multi-Agent) 或高併發伺服器環境中，許多請求共享相同的 System Prompt (前綴)。雖然軟體層面可以實作 Prefix Caching，但在多個模型實例切換時，依賴 OS 或軟體的 PagedAttention 仍會造成巨大的虛擬到實體記憶體映射延遲。

## 解決方案 (HUKV-MMU)
我們提出並模擬了 **硬體統一 KV 快取 MMU (HUKV-MMU)**。
將全域 (Global) 的前綴樹 (Radix Tree / Prefix Tree) 匹配與記憶體分頁管理，直接下放到 Edge NPU 內建的硬體 MMU 中。當不同 Agent 送入相同的系統前綴時，硬體 MMU 會自動命中實體 SRAM/DRAM 分頁，達到零軟體開銷的跨實例快取共享。

## 模擬數據 (hw_unified_kv_cache_mmu_sim.py)
* **Baseline Latency (Software)**: 110.00 ms
* **HUKV-MMU Latency (Hardware)**: 15.00 ms
* **Throughput Speedup**: 7.33x

## 架構建議
建議在支援 Multi-Agent 協作的 Edge NPU 架構中，引入專屬的「統一 KV 快取 MMU」，以極大化 SRAM 的利用率並消除任務切換的延遲瓶頸。