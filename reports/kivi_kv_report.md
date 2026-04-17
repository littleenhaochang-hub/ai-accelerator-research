# KIVI 2-bit KV Cache 量化硬體架構分析

## 實驗背景
為了將 Edge 裝置 (如 Mac mini, AI PC) 的 Context Length 推向極限，除了動態驅逐與架構共用外，將 KV Cache 壓縮至極低位元是必經之路。我們探討了類似 KIVI 的 2-bit KV Cache 量化策略在硬體層面的頻寬與容量效益。

## 實驗方法
撰寫 `kivi_kv_sim.py`，模擬 32K Context 下 2-bit (Group Size = 32) 非對稱量化 KV Cache 的記憶體佔用。我們計算了 2-bit 資料本體以及對應的 Scale/Zero-point 詮釋資料 (Metadata) 所造成的開銷。

## 實驗數據
- **Baseline FP16 KV Cache**: 536.87 MB
- **KIVI 2-bit KV Cache (含 Metadata)**: 100.66 MB
- **Memory Footprint Reduction**: 81.25%
- **Effective Bandwidth Speedup**: 5.33x

## 硬體架構結論
2-bit KV Cache 量化能帶來驚人的 81.25% 記憶體縮減，讓 32K 文本的 KV 佔用從 536MB 暴降至約 100MB，且等效頻寬提升高達 5.33 倍。
為了在邊緣裝置上達成此效益，NPU 必須在 Attention 模組內部安插專屬的 **2-bit KV Decompressor (2位元 KV 解壓縮器)**。這套邏輯電路必須能在讀取 2-bit 資料與其對應的 FP16/FP8 Scales 時，於一個 Cycle 內完成 $x = q \times scale + zero$ 的重建，並無縫餵給 MAC 陣列，才能避免因反量化造成的 Pipeline 停頓。
