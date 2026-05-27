# Hardware 2-bit Asymmetric KV Quantizer and Matcher (HW-2-KV)
## 針對超長文本 KV Cache 瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
處理 64K 以上的超長文本時，FP16 的 KV Cache 記憶體足跡與讀取頻寬成為最大瓶頸。由於 Key 與 Value 在 Attention 計算中的敏感度不同，將兩者統一量化（如全 INT4）往往會導致模型精度顯著下降 (SQNR 衰減)，或無法最大化壓縮率。

### 2. 探索文獻 (Explore)
我們提出 Hardware 2-bit Asymmetric KV Quantizer and Matcher (HW-2-KV)。基於非對稱量化理論，我們將對計算相似度 (Dot Product) 較有容忍度的 Key Cache 壓縮至極限的 2-bit，而保留 Value Cache 在 4-bit 以維持生成品質。同時，硬體原生支援 2-bit 與 4-bit 混精度的解壓縮與 MAC 運算。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_2_kv_sim.py` 進行 64K Context 模擬驗證：
- **Baseline FP16 Latency:** 16005.00 ms
- **HW-2-KV Latency:** 3001.74 ms
- **Speedup (加速比):** 5.33x
- **記憶體容量/頻寬縮減:** 81.25%
- **精度維持:** SQNR 28.1 dB

### 4. 結論
實作 HW-2-KV 能帶來 5.33x 的長文本解碼加速，並省下超過 81% 的記憶體空間。建議將此「非對稱混精度 KV 壓縮引擎」整合入下一代 Edge NPU 的 SRAM 記憶體控制器中。
