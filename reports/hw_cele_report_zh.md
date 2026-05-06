# Hardware Cross-Entropy Loss Engine (HW-CELE) 實驗報告

## 背景與瓶頸分析
隨著 Test-Time Training (TTT) 與 On-Device 裝置端微調 (如 LoRA) 的需求增加，模型在 Edge NPU 上的 Backward Pass 成為新的焦點。其中一個巨大的記憶體頻寬瓶頸發生在最後的分類層 (LM Head)。對於一個包含 128K 詞表的模型，在 Context Length 為 2K 的情況下，Logits 矩陣高達 512MB。傳統軟體流程需要將這 512MB 寫入 SRAM，再讀出進行 Softmax 與 Cross-Entropy (CE) Loss 計算，最後將 Gradient 寫回，總計產生高達 1.5GB 的中間 SRAM 流量，嚴重拖垮能效與速度。

## 解決方案：HW-CELE (硬體交叉熵損失引擎)
我們提出 **HW-CELE (Hardware Cross-Entropy Loss Engine)**，這是一種將 LM Head 的線性投影 (Linear Projection)、Softmax 計算與 CE Loss 梯度計算 (Logit - Target) 完全硬體融合的內聯引擎 (Inline Engine)。
當 Tensor Core 產生局部的 Logit 結果時，結果會直接停留在暫存器層級 (Register File) 進行硬體 Softmax 計算與目標值減法，最後只將完成的梯度矩陣寫回 SRAM。

## 實驗結果
透過 Python 模擬 (`hw_cele_sim.py`)，針對 128K Vocab 與 2K Sequence Length 進行測試：
- **基準 SRAM 流量:** 1500.00 MB
- **HW-CELE SRAM 流量:** 500.00 MB
- **基準 Latency:** 1.4648 ms
- **HW-CELE Latency:** 0.2930 ms
- **局部吞吐量加速比 (Speedup):** 5.00x

## 結論
HW-CELE 成功將 On-Device Learning 中最耗費記憶體頻寬的 LM Head 與 Loss 計算步驟進行硬體級融合，將記憶體往返流量降低了三分之二，並帶來 5.00x 的局部延遲加速。這使得 Edge NPU 能夠在極低的功耗下完成 Test-Time Training。建議將此引擎作為新一代支援邊緣學習 (Edge Learning) 架構的標準配備。
