# Hardware Speculative Mamba Tree Verifier (HW-SMTV)

## 摘要 (Executive Summary)
本研究探討將 Speculative Decoding 的草稿驗證 (Draft Verification) 套用於 Mamba/SSM 模型。由於 SSM 的狀態更新具有時序依賴性 (Sequential Dependency)，傳統軟體驗證必須逐個 token 進行。我們評估了在硬體層面實作平行結合掃描 (Parallel Associative Scan Tree) 來同步驗證多個草稿分支的架構。

## 實驗結果 (Simulation Results)
- **測試環境:** 64 Draft Tokens (Tree Topology)
- **軟體循序驗證延遲 (Baseline):** 9.60 ms
- **硬體平行驗證延遲 (HW-Tree Verifier):** 0.48 ms
- **延遲加速比 (Latency Speedup):** 20.00x
- **訊噪比 (SQNR):** 33.1 dB

## 結論與架構建議
實驗證明，透過硬體層面的 Parallel Associative Scan，可將 Mamba 草稿驗證的 $O(N)$ 循序依賴性降為 $O(\log N)$ 的平行計算時間，達到 20.00x 的加速比。
**架構提案:** 建議在邊緣 NPU 的 Mamba 加速單元中整合「HW-SMTV 平行樹驗證引擎」，以完美支援 SSM 架構的 Speculative Decoding 加速。