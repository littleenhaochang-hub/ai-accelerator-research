# Hardware Activation Delta-Encoding Engine (HW-ADEE) 實驗報告

## 背景與瓶頸分析
在長文本生成或大量連續 Token 處理時，神經網路相鄰 Token 的 Activation (激勵值) 或同一 Token 在相鄰 Layer 的 Activation 往往具有高度的時間與空間相似性。傳統 NPU 在層與層之間傳遞資料時，皆以 Dense (密集) 格式將完整的 FP16 或 INT8 矩陣寫入 SRAM 再讀出，這造成了極大的記憶體頻寬浪費。

## 解決方案：HW-ADEE (硬體激勵增量編碼引擎)
我們提出 **HW-ADEE (Hardware Activation Delta-Encoding Engine)**，一種內嵌於 SRAM 介面的動態壓縮單元。
當 Tensor Core 輸出 Activation 時，HW-ADEE 會將其與前一狀態 (Token 或 Layer) 進行硬體相減，若差異小於預設閾值，則視為零 (Zero)，並轉換為高度稀疏的 Delta 矩陣與 Bitmask 寫入 SRAM。讀取時再由解碼端進行還原。

## 實驗結果
透過 Python 模擬 (`hw_adee_sim.py`)，針對 8K Context 進行測試 (假設 75% 的值具有高相似度可被遮蔽)：
- **基準 SRAM 流量 (讀+寫):** 128.00 MB
- **HW-ADEE SRAM 流量 (包含 Bitmask):** 40.00 MB
- **基準 Latency:** 0.0625 ms
- **HW-ADEE Latency:** 0.0195 ms
- **吞吐量加速比 (Speedup):** 3.20x

## 結論
HW-ADEE 利用資料的空間與時間局部性，在不改變模型權重結構的前提下，透過硬體層級的 Delta Encoding 將 SRAM 內部頻寬需求降低了超過 68%。這使得 NPU 能夠將寶貴的 SRAM 頻寬分配給 Weight Fetching，大幅改善 Compute-Bound 模型在 Edge 裝置上的整體能效與吞吐量。
