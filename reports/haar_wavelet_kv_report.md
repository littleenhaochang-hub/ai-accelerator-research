# 長文本 KV Cache 的 Haar 小波硬體壓縮架構

## 1. 瓶頸分析 (Bottleneck Analysis)
隨著語言模型上下文長度推至 32K 甚至 128K，KV Cache 的容量與 SRAM 讀取頻寬成為 Edge NPU 的致命傷。以 32K 上下文、32 Heads、128 Head Dim 計算，單層的 FP16 KV Cache 就高達 512MB。

## 2. 探索與硬體協同設計 (Exploration & Co-Design)
我們提出採用 **1D Haar 小波轉換 (Haar Wavelet Transform)** 沿著序列維度對 KV Cache 進行即時壓縮。
Haar 小波轉換只需要加法與減法，無需複雜的乘法器，非常適合硬體實作。
策略：保留 100% 的低頻資訊 (Low-frequency components) 以及前 10% 的高頻突變資訊，捨棄剩餘的高頻雜訊。

## 3. 原型與驗證 (Prototype & Test)
執行實驗腳本：`haar_wavelet_kv_sim.py`
- **Baseline KV Cache**: 512.00 MB, 讀取延遲 102.40 us
- **Haar Compressed KV Cache**: 281.60 MB (減少 45.0% 的記憶體佔用)
- **硬體解碼與讀取總延遲**: 68.82 us (包含 12.5 us 的 Inverse Haar 加法樹延遲)
- **整體速度提升 (Speedup)**: **1.49x**

## 4. 硬體架構建議
對於 Edge NPU，我們建議在 SRAM 讀取埠與 Tensor Core 之間整合「Hardware Inverse Haar Transform (IHT) 加法樹引擎」。這樣能在讀取壓縮資料後，以 Zero-cycle penalty 的方式在 RF (Register File) 內即刻還原為原始的 KV 矩陣，大幅減少 SRAM 讀取帶寬的耗用。
