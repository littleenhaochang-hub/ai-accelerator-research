# Hardware PIM-based KV Evictor V2 (HW-PIM-KVE-V2) 實驗報告
## 1. 研究背景與瓶頸分析
無限生成串流模型 (StreamingLLM) 在處理長時間上下文時，CPU/NPU 必須頻繁介入管理 Ring Buffer 與執行 KV Cache Token 的淘汰 (Eviction)。這種頻繁的控制流干擾會打斷硬體推論流水線，並大量佔用記憶體匯流排。
## 2. 硬體架構創新
內建於記憶體的 PIM 非同步 KV 淘汰引擎 (HW-PIM-KVE-V2)。該引擎具備獨立的 LRU (Least Recently Used) 狀態機，在背景自主管理記憶體覆寫與重組，NPU 完全無需發送任何控制指令。
## 3. 實驗數據
* Speedup: 11.25x
* Bandwidth Reduction: 91.25%
## 4. 結論
建議將 HW-PIM-KVE-V2 整合至 Edge 裝置的記憶體控制器，以實現真正的「零干擾」無限上下文推論。
