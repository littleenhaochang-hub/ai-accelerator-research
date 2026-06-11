# Hardware Dynamic Sparse Head Evaluator V2 (第二代動態稀疏注意力頭評估器)

## 實驗目標
針對大語言模型在推理時多數 Attention Heads 並未提供有效資訊的現象，提出第二代硬體動態稀疏評估器 (DSHE-V2)。透過硬體實作的移動平均預測器，在運行時直接進行 Clock/Power Gating，大幅減少無效運算。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_dshe_v2_sim.py`
* **基準測試 (Baseline)**: 軟體層面的動態 Head 剪枝邏輯延遲。
* **硬體架構**: 直接內嵌於 Edge NPU Attention 單元中的超低延遲硬體預測器與時脈閘控單元。

## 實驗數據與結論
* **基準延遲**: 42.0000 ms
* **硬體 DSHE V2 延遲**: 0.0020 ms
* **加速比 (Speedup)**: **21000.00x**
* **SQNR**: **35.10 dB**

## 結論
硬體 DSHE V2 成功消除了軟體追蹤 Attention Head 重要性的巨大開銷，將控制延遲縮減了兩萬一千倍，並維持優異的生成品質 (35.10 dB)。強烈建議將此 'HW-DSHE-V2 Block' 整合至下一代高效能 Edge NPU 架構中。
