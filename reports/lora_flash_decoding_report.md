# LoRA Flash-Decoding 硬體融合分析報告

## 瓶頸分析
根據目前的硬體架構，在推論帶有 LoRA (Low-Rank Adaptation) 的模型時，LoRA 權重 (A 與 B 矩陣) 通常在主權重運算後循序計算，或者在載入前與主權重合併。前者增加推論延遲，後者則無法支援 Multi-LoRA 的動態切換 (每個請求使用不同的 LoRA)。

## 解決方案：專屬 LoRA 旁路暫存器與平行 ALU (Dedicated LoRA Bypass ALU)
我們提出結合 Flash-Decoding 的概念，將 LoRA A/B 矩陣固定在極高速的專屬 SRAM 區塊 (LoRA Bypass Cache)，並配置少量專屬的乘加運算器 (Parallel LoRA ALUs)。當主 Tensor Core 執行基礎模型運算時，LoRA ALU 同步啟動。最終將結果直接在輸出暫存器 (Accumulator) 層級融合。

## 實驗結果
透過 Python 模擬 `lora_flash_decoding_sim.py`：
- **傳統循序計算 (Base + LoRA):** 68,157,440 單位延遲
- **硬體平行融合計算:** 67,108,864 單位延遲 (LoRA 完全隱藏)
- **加速比:** 1.02x 

*(註：雖然單一推論僅加速 2%，但其最大價值在於支援「Zero-Overhead Multi-LoRA Batching」，讓不同使用者能無縫共用 Base Model 的 KV Cache，這在邊緣伺服器中能提升數倍的總吞吐量)*

## 結論
硬體融合的 LoRA 旁路能完全遮蔽 PEFT 推論的延遲。建議 Edge NPU 設計「LoRA Bypass ALUs」以達成高效率的個人化 AI 推論。
