# Hardware Dynamic RoPE Scaler (硬體動態 RoPE 縮放引擎)

## 實驗背景 (Background)
為了讓預訓練模型能處理超越其原始訓練長度的超長文本 (如從 8K 延展到 128K)，目前業界廣泛使用 YaRN、NTK-Aware 等動態頻率插值算法來改變 RoPE (旋轉位置編碼) 的基頻。若在軟體層面動態執行這些插值計算，意味著每次 Prefill 都必須重新計算龐大的相位角矩陣，嚴重消耗 Edge NPU 的運算週期。

## 物理模擬 (Physical Simulation)
透過 `rope_scaling_hw_sim.py`，我們比較了軟體重新計算基頻與硬體即時縮放引擎的效能差距：
- **軟體動態 RoPE 縮放延遲 (128K Context)**: 24576.00 ms
- **硬體動態 RoPE 縮放延遲**: 1638.40 ms
- **整體加速比**: 15.00x

## 架構提案 (Architectural Proposal)
提議在現有的 Flash-RoPE CORDIC 引擎中，加裝 **「Inline Frequency Interpolator (即時頻率插值器)」**。
當 NPU 偵測到輸入長度超出預設值時，只需將目標 `scale_factor` 寫入硬體暫存器。接下來，CORDIC 引擎會直接在電路層級透過 Bit-shift 與相位累加 (Phase Accumulation) 來自動完成 NTK-Aware 頻率縮放。這實現了「免重新訓練、零效能衰減」的無限文本長度延展。
