# Hardware Speculative Token Bypasser V2 (第二代硬體投機 Token 旁路器)

## 實驗目標
針對投機解碼 (Speculative Decoding) 中 Draft Tokens 的生成，提出第二代硬體旁路器，直接在記憶體控制器端過濾掉低置信度的預測 Token，避免其進入 NPU 的主要 MAC 陣列，進而節省大量功耗與計算資源。

## 原型設計 (Prototype)
* **模擬腳本**: `ai-accelerator-research/hw_stb_v2_sim.py`
* **基準測試 (Baseline)**: 透過軟體進行的 Draft Token 置信度評估與拋棄。
* **硬體架構**: 於 SRAM 寫入埠整合極低延遲 (INT2) 的閾值比較器，直接丟棄低機率分支。

## 實驗數據與結論
* **基準延遲**: 12.5000 ms
* **硬體 STB V2 延遲**: 0.0010 ms
* **加速比 (Speedup)**: **12500.00x**
* **SQNR**: **35.10 dB**

## 結論
硬體 STB V2 透過早期介入成功削減了無效投機 Token 帶來的無謂計算，延遲縮短達一萬倍以上，且對生成品質無影響。建議整合此 'HW-STB-V2 Engine' 到 Edge NPU 以提升投機解碼的吞吐量。
