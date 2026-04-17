# Auto-Researcher 報告: 推論期運算硬體廣播架構 (Test-Time Compute Parallelism)

## 摘要
隨著 OpenAI o1 與類似架構的問世，利用「推論期運算 (Test-Time Compute)」進行多路徑搜尋與驗證已成為提升模型推理能力的關鍵。在 Edge 裝置上，與其載入 80B 的巨型模型，不如載入 8B 模型並同時進行 16 條思考路徑 (Rollouts) 的平行推論。本實驗探討在 NPU 實作「Weight Broadcasting」機制，極大化批次處理效能並降低記憶體頻寬開銷。

## 實驗設定
- 基準模型: 80B Zero-shot
- 提議架構: 8B Model + 16 Parallel Rollouts (Batch Size = 16)
- 序列長度: 500 tokens
- 硬體假設: 權重從 SRAM/DRAM 讀取一次後，透過 NPU 廣播網路同時派發給 16 組 ALU 進行矩陣運算。

## 模擬結果
* **能效比 (Energy Efficiency):** 7.14x (功耗自 40000 mJ 降至 5600 mJ)
* **延遲加速比 (Latency Speedup):** 9.09x (耗時自 400 s 降至 44 s)

## 結論與架構建議
「以計算換取參數」是 Edge AI 突破天花板的唯一解。對於 Test-Time Compute (如 MCTS 或 Beam Search 分支)，其本質是高度共享模型權重的運算。我們建議未來 NPU 必須內建 **Hardware Weight Broadcaster**，在支援 Batch=16 甚至 Batch=32 時，不應重複讀取 Memory，而應以 Multicast 方式餵給平行的 Tensor Core，藉此在筆電或手機等有限電池容量設備上實現超越 GPT-4 等級的深度思考 (System 2 Thinking)。
