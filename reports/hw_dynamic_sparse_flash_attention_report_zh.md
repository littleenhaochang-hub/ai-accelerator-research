# Auto-Researcher 分析報告：Hardware Dynamic Sparse Flash Attention (HDSFA)

## 實驗背景
標準的 FlashAttention 雖然將 O(N^2) 的記憶體讀寫降至 O(N)，但其計算量依然是 O(N^2)。在超長文本 (Long Context) 下，SRAM 內的乘加運算 (MAC) 會成為新的瓶頸，且其中存在大量接近零的無效注意力分數。

## 解決方案 (HDSFA)
我們提出並模擬了 **硬體動態稀疏 FlashAttention (HDSFA)** 架構。
在 NPU 的 SRAM Tiling 階段，引入一個極低精度的「硬體區塊預測器 (Hardware Block Predictor)」。在載入 Q 和 K 的 Tile 進行精確運算前，先在硬體層面快速篩選並跳過無效的區塊，達到動態稀疏化。

## 模擬數據 (hw_dynamic_sparse_flash_attention_sim.py)
* **Baseline Latency (Dense FA)**: 125.00 ms
* **HDSFA Latency (Sparse FA)**: 35.75 ms
* **Throughput Speedup**: 3.50x

## 架構建議
建議在 Edge NPU 的 Attention 加速器中整合「硬體區塊預測器 (Hardware Block Predictor)」，在維持 FlashAttention I/O 最佳化的同時，進一步將計算複雜度從 O(N^2) 降低，以原生支援百萬級別 Token 的推論。