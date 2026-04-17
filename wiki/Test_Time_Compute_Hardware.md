# Test-Time Compute: Early-Exit Hardware Pipeline

## 實驗背景
Test-Time Compute (TTC) 透過 Early-Exit 等機制減少推論算力。然而，動態退出會破壞 Batch 推論的規律性，導致 NPU 產生 Pipeline 氣泡。

## 硬體模擬與分析
- **腳本**: `test_time_compute_sim.py`
- 模擬顯示，雖然理論上平均運算量可大幅降低，但在考量硬體 Pipeline 閒置懲罰 (30%) 後，實際加速比從理想的 2.66x 降至 **2.05x**。

## 架構協同設計結論
Edge AI 晶片要支援高效的 TTC，硬體排程器 (Hardware Scheduler) 必須升級為支援「亂序執行 (Out-of-Order Execution)」與內建 **Dynamic Token Routing Buffer**。這能讓提早退出的 Token 脫離 Pipeline，並將剩餘 Token 重新打包，消除計算氣泡。
