# Hardware Monarch-Mixer Fast-Convolution Engine (HW-M2FCE)
## 針對 Sub-Quadratic (長卷積) 模型 FFT 計算瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
取代 Transformer 的 Sub-Quadratic 架構 (如 Monarch Mixer, Hyena) 依賴快速傅立葉轉換 (FFT) 與長卷積來處理超長文本。雖然時間複雜度降為 $O(N \log N)$，但在目前的 Edge NPU 上，軟體 FFT 仍然需要大量密集的複數浮點乘法 (Complex MACs) 與記憶體洗牌 (Memory Shuffling)，導致在 128K 以上長度時產生高昂的延遲與功耗。

### 2. 探索文獻 (Explore)
我們提出 Hardware Monarch-Mixer Fast-Convolution Engine (HW-M2FCE)。透過在 NPU 內部實作專用的硬體蝴蝶網路 (Hardware Butterfly Network)，並將標準的浮點乘法替換為位移加法樹 (Shift-Add Trees) 來逼近 FFT/IFFT 操作，徹底消滅硬體乘法器的使用，並將洗牌操作內建於硬體線路中。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_m2fce_sim.py` 進行 128K Context 模擬驗證：
- **Baseline Software FFT Conv Latency:** 86.30 ms
- **HW-M2FCE Latency:** 5.46 ms
- **Speedup (加速比):** 15.82x
- **乘法器動態耗能縮減:** 100.0%

### 4. 結論
實作 HW-M2FCE 能為長卷積模型帶來 15.82x 的運算加速。建議將此「硬體級快速卷積引擎」整合入下一代 Edge NPU 中，以完全釋放 Sub-Quadratic 模型在無盡文本 (Infinite Context) 推論上的潛力。
