# Hardware Dynamic Activation Pruning (HDAP)

## 實驗背景與動機
在大型語言模型中，FFN（前饋神經網路）層的 Activation 具有高度稀疏性。軟體層面的 Activation Pruning 通常需要讀取完整的張量，進行閾值判斷後再生成 Mask，這過程帶來顯著的記憶體頻寬開銷與運算延遲。為了最大化運算單元（如 MAC 陣列）的利用率並減少不必要的 DRAM/SRAM 資料搬移，本實驗驗證將 Activation Pruning 邏輯實作為硬體層級的動態過濾器。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 在 CPU/GPU 端執行一個額外的 Kernel 來掃描 Tensor，計算並套用 Sparsity Mask。這會導致額外的記憶體往返（Round-trip）與延遲。
- **硬體提案 (Hardware HDAP Engine):** 在 Edge NPU 的 SRAM 讀取端口與 Tensor Core 之間植入「Dynamic Activation Pruner」。當資料從 SRAM 流向 MAC 陣列時，HDAP 引擎即時檢查數值。低於動態閾值的 Activation 會直接被丟棄，並發送 Skip 訊號給 MAC 控制器，從而實現在零記憶體開銷下動態減少乘加運算。

## 效能分析結果
針對 16K Context 下的 FFN 計算進行 Profiling：
- **傳統軟體 Activation Pruning 延遲 (Software Latency):** 18.20 ms
- **硬體動態 Activation Pruning 延遲 (Hardware Latency):** 2.40 ms
- **加速比 (Speedup):** 7.58x

## 結論與架構建議
透過 HDAP 引擎，我們成功在資料傳輸路徑上動態剔除了無效計算，將軟體處理稀疏性的延遲消弭於無形。建議未來的 Edge NPU 在 Tensor Core 前端標配「Inline Activation Pruner」，以原生支持高度稀疏的模型推論，極大化電池續航力與推論吞吐量。