# Hardware Flash-RoPE Engine (硬體 RoPE 旋轉引擎)

## 實驗背景 (Background)
旋轉位置編碼 (Rotary Position Embedding, RoPE) 是目前多數 LLM 的標準配備。但在極長文本 (如 16K 以上) 的 Prefill 階段，為每一個 Query 和 Key 計算並乘上 Sine/Cosine 值，會佔用大量的 Tensor Core 週期與記憶體頻寬。這變成了 Attention 計算前的一項隱形「運算稅」。

## 物理模擬 (Physical Simulation)
透過 `flash_rope_hw_sim.py`，比較了標準軟體/MAC運算 RoPE 與硬體 CORDIC 引擎的效能：
- **標準 RoPE 延遲 (16K Context)**: 4194.30 ms
- **硬體 Flash-RoPE 延遲**: 104.86 ms
- **整體加速比**: 40.00x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 Attention ALU 前端的 SRAM Read Path 路上，加裝 **「Flash-RoPE CORDIC Engine」**。
該引擎使用 CORDIC 演算法，在 Q/K 向量從 SRAM 讀取出來的瞬間，於傳輸流中即時 (On-the-fly) 完成旋轉計算，再送入主運算陣列。這將 RoPE 的計算時間完全隱藏在記憶體讀取延遲中，實現對主 MAC 陣列的「零開銷 (Zero-overhead)」加速。
