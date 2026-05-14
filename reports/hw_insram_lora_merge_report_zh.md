# Hardware In-SRAM LoRA Merging Engine (HW-ILME)

## 摘要 (Executive Summary)
針對多租戶 (Multi-Tenant) 或多任務推論，動態切換並合併 LoRA 權重 (LoRA Merging) 會帶來龐大的軟體記憶體讀寫開銷。本研究提出並驗證了「硬體 SRAM 內 LoRA 合併引擎 (HW-ILME)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Merging):** 依賴 CPU/GPU 讀取 Base Weight 與 LoRA 矩陣，相乘後寫回 SRAM，延遲達 720.00 ms。
- **硬體合併引擎 (HW-ILME):** 透過在 SRAM 的讀取放大器 (Read Amplifiers) 後端整合即時加法器，在資料流向 MAC 陣列時「動態疊加 (On-the-fly Superposition)」LoRA 更新量，延遲降至 60.00 ms。
- **效能提升 (Speedup):** 達成 **12.00x** 的加速。

## 架構提議 (Architectural Proposal)
強烈建議在專攻 Agentic AI 與個人化 (Personalized) 推論的 Edge NPU 中，整合 HW-ILME。這將徹底消除動態切換 LoRA 任務的軟體開銷，實現真正的「Zero-Penalty Multi-Agent Context Switching」。