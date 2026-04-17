# Cross-Layer Attention (CLA) KV Cache Hardware Analysis

## 實驗背景
為了解決極長文本 (Extreme Long Context) 下的 KV Cache 記憶體容量耗盡問題，除了低位元量化外，架構層面的改進也是關鍵。我們測試了 Cross-Layer Attention (CLA) 的硬體實作效益，即讓相鄰的多個 Transformer Layer 共用同一組 KV Cache，進而從架構上成倍減少記憶體佔用。

## 實驗方法
撰寫 `cross_layer_kv_sim.py`，模擬 32 層 Transformer 模型在 8K Context 下，設定 Group Size 為 4 (每 4 層共用一組 KV) 的記憶體佔用與繞線 (Routing) 延遲開銷。

## 實驗數據
- **Baseline KV Cache Memory (32 Layers)**: 4294.97 MB
- **CLA KV Cache Memory (Group Size 4)**: 1073.74 MB
- **Memory Footprint Reduction**: 75.00%
- **Effective Bandwidth Speedup**: 3.38x

## 硬體架構結論
CLA 架構能直接使 KV Cache 容量需求降低至原本的 $1/N$ (此例中為 1/4)，且能帶來 3.38 倍的記憶體存取加速。
在硬體設計上，雖然容量減少，但會面臨同一個 SRAM Block 必須同時/依序將 KV 資料傳送給不同 Layer 的 Attention 單元的問題。因此，必須在 Edge NPU 的 SRAM 讀取埠增加專用的 **KV Route Multiplexer (KV 繞線多工器)** 與 **Broadcaster**，才能實現無延遲的跨層資料廣播。
