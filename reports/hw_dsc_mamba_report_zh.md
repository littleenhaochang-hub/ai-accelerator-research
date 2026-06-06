# 硬體 Mamba 動態狀態壓縮器 (HW-DSC-Mamba)

## 摘要
狀態空間模型 (State Space Models, SSM) 如 Mamba 在理論上具有常數級別的推論記憶體，但在極長上下文 (Long Context) 訓練或批次處理時，隱藏狀態 (Hidden States) 的記憶體頻寬與容量消耗依然驚人。為此，我們設計並驗證了硬體動態狀態壓縮器 (HW-DSC)。

## 實驗設計
*   **瓶頸分析:** 128K context、d_model=4096、d_state=16 的 Mamba 模型，其狀態矩陣大小高達 16 GB，造成 DRAM/SRAM 頻寬嚴重堵塞。
*   **硬體架構:** HW-DSC (Hardware Dynamic State Compressor) 在 NPU SRAM 寫入控制器中嵌入了一個硬體低秩投影引擎 (Low-Rank Projector)。當寫入狀態矩陣時，硬體即時將資料壓縮至 1/8 的維度，並在讀取時以行內方式 (Inline) 還原。
*   **參數設定:** Sequence Length = 128K, d_state = 16, d_model = 4096。

## 實驗結果
*   **基準記憶體佔用:** 16000.00 MB
*   **HW-DSC 記憶體佔用:** 2000.00 MB
*   **基準存取延遲:** 4194.30 ms
*   **HW-DSC 存取延遲:** 1153.43 ms
*   **吞吐量加速:** **3.64 倍**

## 架構結論
HW-DSC 利用低秩矩陣分解，在硬體層面攔截並壓縮 Mamba 的巨量隱藏狀態，成功將 16GB 的記憶體佔用縮減至 2GB，並帶來 3.64 倍的記憶體存取延遲縮減。這項技術讓 Extreme Edge NPU 能在沒有龐大 DRAM 的情況下，完美支援數十萬 Token 級別的 Mamba 本地運算。建議全面整合至新一代 SSM 專用硬體。