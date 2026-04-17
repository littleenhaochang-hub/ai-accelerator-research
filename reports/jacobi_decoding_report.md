# Jacobi / Lookahead Decoding 硬體平行化分析

## 實驗背景
為了解決 LLM 生成階段 (Decoding) 序列依賴造成的低吞吐量問題，我們測試了不依賴 Draft Model 的非自迴歸平行解碼演算法 (Jacobi Decoding / Lookahead Decoding)。此方法試圖將未來的多個 Tokens 作為 N-gram 軌跡一次性平行計算，並透過多次迭代收斂。

## 實驗方法
撰寫 `jacobi_decoding_sim.py` 模擬並行解碼 12 個 Tokens 的運算延遲。
- **Trajectory Window**: 4 tokens
- **Iterations to converge**: 4次 (平均)
- 比較標準 Auto-regressive (AR) 與並行 GEMV 的總延遲。

## 實驗數據
- **Baseline AR Latency**: 180.00 ms
- **Jacobi Parallel Latency**: 192.00 ms
- **Effective Speedup**: 0.94x (發生效能倒退)

## 硬體架構結論
實驗宣告**失敗/效能倒退**。儘管 Jacobi Decoding 在理論上能增加 MAC 利用率，但在實際硬體上，因多次迭代 (Iterations) 造成的記憶體重複讀取與運算開銷，超過了平行化帶來的時間節省。
**硬體架構建議**：純軟體的 Jacobi Decoding 對於 Edge NPU 並不實用。若要使其發揮作用，硬體 SRAM 內部必須增加 **Multi-Token Dependency Forwarding (多 Token 依賴轉發邏輯)**，在不用回傳給 Main Memory 的情況下，讓猜測的隱藏狀態 (Hidden States) 之間直接在暫存器層級進行通訊與校正。在具備此硬體前，建議維持使用 Speculative Decoding。
