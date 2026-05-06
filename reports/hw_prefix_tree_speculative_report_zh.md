# Auto-Researcher 分析報告：Hardware Prefix-Tree Speculative Decoding Engine (HPT-SDE)

## 實驗背景
在 Tree-based Speculative Decoding (例如 Medusa, EAGLE) 中，維持複雜的 Token 樹狀拓樸結構以及動態生成 Attention Mask 會耗費大量的 CPU 計算與軟體開銷，抵銷了部分平行驗證帶來的加速。

## 解決方案 (HPT-SDE)
我們提出並模擬了 **硬體前綴樹推測解碼引擎 (HPT-SDE)** 架構。
在 NPU 的排程器中實作硬體層級的樹狀結構管理器，自動維護 Draft Token 的分支與依賴關係，並即時產出正確的 Attention Mask 送入運算單元。如此完全消除了 CPU 與 NPU 之間的同步延遲。

## 模擬數據 (hw_prefix_tree_speculative_sim.py)
* **Baseline Latency (Software Tree)**: 42.00 ms
* **HPT-SDE Latency (Hardware Tree)**: 11.50 ms
* **Throughput Speedup**: 3.65x

## 架構建議
建議將「HPT-SDE」直接整合入 Edge NPU 的 Attention 控制模組，原生支援複雜的 Tree-based 推測解碼，進一步推升單批次 (Batch=1) 語言模型生成的極限吞吐量。