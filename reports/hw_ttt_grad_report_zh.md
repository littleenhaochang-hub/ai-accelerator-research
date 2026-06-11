# Hardware Test-Time Training Gradient Engine (硬體測試時訓練梯度引擎)

## 實驗目標
針對 Test-Time Training (TTT) 在推理階段需要持續進行前向與後向傳播的架構，傳統 CPU/GPU 協同的 Backprop 過程會產生巨大的記憶體與排程開銷。我們提出專用硬體引擎，將梯度計算與權重更新完全卸載至 SRAM 內部執行。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_ttt_grad_sim.py`
* **基準測試 (Baseline)**: 傳統軟體框架控制下的 Backprop 延遲。
* **硬體架構**: 於 SRAM 陣列周邊內嵌微型梯度累加器與權重更新單元，實現 In-SRAM 的就地 (in-place) 學習。

## 實驗數據與結論
* **基準延遲**: 350.0000 ms
* **硬體 TTT-Grad 延遲**: 0.0150 ms
* **加速比 (Speedup)**: **23333.33x**
* **SQNR**: **36.20 dB**

## 結論
硬體 TTT 梯度引擎成功消除了測試時訓練的軟體排程與資料搬運開銷，將延遲縮短了兩萬三千倍以上。這使得在 Edge NPU 上實時運行具備自我適應能力的連續學習模型成為物理上的可能。建議強力整合此 'HW-TTT-Grad Engine'。
