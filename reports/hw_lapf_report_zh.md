# Hardware LoRA Adapter Pre-Fetcher (HW-LAPF)

## 實驗背景 (Background)
在多租戶 (Multi-tenant) 或多代理 (Multi-agent) 系統中，需要頻繁切換不同的 LoRA Adapter。傳統的按需載入 (Demand Fetch) 會造成嚴重的阻塞延遲。

## 實驗設計 (Methodology)
本實驗設計了硬體級別的 LoRA 預先載入器 (`hw_lapf_sim.py`)。透過分析排程器中的請求佇列，HW-LAPF 會在背景透過異步 DMA 預先將下一個 Agent 需要的 LoRA 權重載入到 SRAM 專用區塊中，完美重疊運算與記憶體傳輸時間。

## 實驗結果 (Results)
- Demand LoRA Fetch Latency: 0.5500 s
- HW-LAPF Prefetch Latency: 0.0100 s
- **Speedup**: 55.00x

## 硬體提案 (Hardware Proposal)
建議在 Edge NPU 的 DMA Controller 內建「HW-LAPF 引擎」。這能將 Multi-Agent 系統的 Context Switch 延遲縮減 98%，實現真正無縫的本地端多重 Agent 協作。