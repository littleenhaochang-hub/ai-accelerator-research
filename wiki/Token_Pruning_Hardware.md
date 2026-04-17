# Dynamic Token Pruning Hardware Architecture

## 實驗背景
Token Pruning 藉由在每一層動態丟棄較無資訊量的 Tokens，能大幅降低深層網路的算力需求。

## 硬體模擬與分析
- **腳本**: `token_pruning_sim.py`
- 設定每層丟棄 5% tokens，經過 24 層後，Token 數量從 4096 降至 1190。
- 總計算量減少，達成 **1.70x** 的推論加速。

## 架構協同設計結論
Edge NPU 需要加入 **Dynamic Memory Compaction (動態記憶體壓縮)** 單元。由於丟棄的 Tokens 散落各地，如果不作壓縮，硬體只會讀取到一堆氣泡 (bubbles) 浪費頻寬。透過支援硬體級別的 Gather-Scatter DMA，可以在層與層之間自動重組連續的 Tensor 記憶體佈局。
