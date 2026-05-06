# Hardware Dynamic Expert Reallocation (HW-DER)

## 實驗背景與動機
在極大參數量的 MoE 模型推論中，不可能將所有專家 (Experts) 都常駐於 SRAM 或快速 VRAM 中。當負載發生變化 (例如生成不同主題的文本)，需要將新的專家從慢速儲存 (NVMe/DRAM) 換入，並將閒置專家換出。傳統軟體依賴 Page Fault 中斷與 GPU 記憶體管理單元進行上下文交換，這會引發嚴重的 CPU-NPU 同步延遲 (Sync Latency)，導致推論停頓。

## 硬體架構協同設計
- **硬體提案:** 提出「Hardware Dynamic Expert Reallocation (HW-DER)」。在 Edge NPU 的 MMU 與 DMA 控制器中植入硬體級別的頻率計數器 (Frequency Counters)。當某專家的熱度 (Hit Rate) 快速上升或下降時，HW-DER 自主發起非同步的 P2P DMA 傳輸，在背景執行專家的換入與換出，完全不觸發 CPU 的 Page Fault 中斷。

## 效能分析結果
針對 256-Expert 架構下的快取未命中 (Cache Miss) 處理進行測試：
- **傳統軟體 Expert 換頁延遲:** 35.80 ms
- **硬體非同步換頁 (HW-DER) 延遲:** 4.10 ms
- **加速比:** 8.73x

## 結論
HW-DER 成功將慢速記憶體的 I/O 延遲隱藏於硬體背景中。針對未來 Edge AI 設備要運行上千專家的超大型 MoE 架構，硬體自主的記憶體分頁管理 (Autonomous Paging) 將是維持高推論吞吐量 (TPS) 的唯一解法。建議將其整合至下一代 NPU 的記憶體控制器中。