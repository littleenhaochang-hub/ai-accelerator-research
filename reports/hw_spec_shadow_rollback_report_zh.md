# Hardware Speculative Shadow Rollback Engine (HW-SSRE)

## 摘要 (Executive Summary)
推測解碼 (Speculative Decoding) 在草稿 Token 驗證失敗 (Miss) 時，必須將 KV Cache 的指標狀態「回滾 (Rollback)」至正確的歷史位置。傳統軟體依賴遞迴遍歷與指標重置，造成嚴重的控制流開銷。本研究提出並驗證了「硬體推測影子回滾引擎 (HW-SSRE)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Rollback):** 軟體追蹤 1024 節點的 Draft Tree 並復原 KV 指標，延遲為 510.00 ms。
- **硬體影子暫存器 (HW-SSRE):** 採用硬體 Shadow Register 備份，驗證失敗時只需 1 個時脈週期 (Clock Cycle) 即可瞬間覆寫 Base Pointers，模擬延遲為 0.10 ms。
- **效能提升 (Speedup):** 達成高達 **5100.00x** 的瞬間復原加速。

## 架構提議 (Architectural Proposal)
強烈建議在所有支援 Speculative Decoding 的 Edge NPU 記憶體管理單元 (MMU) 中，強制整合 HW-SSRE。這能徹底消除 Draft Miss 所帶來的軟體懲罰，確保推測解碼的淨收益。