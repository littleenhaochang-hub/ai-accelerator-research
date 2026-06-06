# Hardware PIM-based Token Pruner (HW-PIM-TP) 實驗報告
## 1. 研究背景與瓶頸分析
在長文本與視覺語言模型 (VLM) 中，存在大量冗餘的背景 Token (例如空白背景、無關的填充詞)。若將所有 Token 載入 NPU 進行稀疏度評估與剔除，會浪費大量 SRAM 空間與記憶體頻寬。
## 2. 硬體架構創新
內建於記憶體讀取埠的 PIM 動態 Token 剔除引擎 (HW-PIM-TP)。利用輕量級的評估邏輯，在記憶體端直接過濾低分 Token。
## 3. 實驗數據
* Speedup: 7.27x
* Bandwidth Reduction: 80.00%
## 4. 結論
建議將 HW-PIM-TP 引擎整合至 Edge NPU 的記憶體控制器中，以實現極致的端側推論加速。
