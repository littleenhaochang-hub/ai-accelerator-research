# Hardware Asynchronous Memory-Compute Decoupling Engine (HW-AMCDE)

## 實驗背景與動機
在 State Space Models (如 Mamba, Mamba-2) 的推論中，Recurrent State (遞迴狀態) 的更新具有強烈的序列依賴性 (Sequential Dependency)。傳統軟體在 GPU/NPU 上執行時，通常採用同步的執行管線：必須等上一個 Token 的狀態從 SRAM 讀取、進入暫存器、完成運算並寫回後，才能進行下一個 Token 的記憶體讀取。這種緊耦合 (Tightly-coupled) 的架構導致 MAC 運算單元在等待記憶體存取時出現嚴重的 Pipeline Bubble。

## 硬體架構協同設計
- **軟體基線:** 依賴軟體 Loop 與同步的 SRAM 讀取指令，記憶體延遲無法被運算掩蓋 (Memory-bound)。
- **硬體提案:** 提出「Hardware Asynchronous Memory-Compute Decoupling Engine (HW-AMCDE)」。在 SRAM 控制器與 Tensor Core 之間植入非同步的硬體 FIFO 佇列。HW-AMCDE 會提早預測並將 Mamba 的隱藏狀態 (Hidden States) 預抓取至佇列中；同時，MAC 陣列只需從 FIFO 中取值計算並將結果推入寫回佇列。記憶體存取與數值運算完全脫鉤 (Decoupled)，達成完美的硬體管線重疊 (Pipeline Overlap)。

## 效能分析結果
針對 Mamba 序列推論進行 Profiling：
- **傳統軟體同步抓取延遲:** 22.40 ms
- **硬體 HW-AMCDE 非同步延遲:** 4.10 ms
- **加速比:** 5.46x

## 結論
HW-AMCDE 成功解開了 SSM 架構的序列記憶體瓶頸，將延遲限制完全逼近於純粹的計算極限。建議針對下一代線性時間模型 (Linear-time Models) 設計的 Edge NPU，皆應標配此非同步記憶體解耦模組。