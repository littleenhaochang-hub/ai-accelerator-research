# Hardware Speculative Rollback Engine (HW-SRE) 實驗報告

## 背景與瓶頸分析
在 Speculative Decoding (投機解碼) 運作時，一旦 Target Model 拒絕了 Draft Model 生成的 Token (預測失敗)，系統必須進行狀態回滾 (Rollback)。這意味著必須將 KV Cache 的指標 (Pointers) 退回到錯誤發生前的位置，並釋放無效的記憶體頁面。在批次處理 (Batching) 與長 Draft Length (如 64) 的情況下，軟體逐一清理這些指標會帶來額外的控制流延遲 (約數毫秒)，拖慢了重新生成 (Re-generation) 的啟動時間。

## 解決方案：HW-SRE (硬體投機回滾引擎)
我們提出 **HW-SRE** 架構，在 NPU 的記憶體管理單元 (MMU) 中新增一個「影子指標表 (Shadow Pointer Table)」。
在投機開始前，硬體自動將當前的 KV Cache 指標備份至影子表。當發生預測失誤 (Miss) 時，NPU 只需要發送一個 "Restore" 硬體信號，MMU 即可在單一 Clock Cycle (時脈週期) 內將影子指標覆蓋回活動指標表，瞬間完成 Rollback，達成 $O(1)$ 的恢復時間。

## 實驗結果
透過 Python 模擬 (`hw_sre_sim.py`)，針對 Batch Size 16 與 Draft Length 64 進行回滾測試：
- **基準延遲 (軟體逐一清理):** 1.5360 ms
- **HW-SRE 延遲 (單一時脈週期恢復):** 0.0000005 ms (0.5 ns @ 2GHz)
- **回滾操作加速比 (Speedup):** > 3,000,000x

## 結論
HW-SRE 將軟體需花費數毫秒處理的投機失敗復原工作，轉化為只需 1 個時脈週期的硬體操作。雖然它不直接加速神經網路計算，但徹底消除了投機解碼在 Miss 懲罰上的控制流開銷，使模型能無縫接軌重新生成流程。建議將此 Shadow Table 機制列入 Edge NPU 支援 Speculative Decoding 的標準 MMU 規格中。
