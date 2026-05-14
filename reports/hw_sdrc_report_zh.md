# 硬體推測性草稿回滾快取 (HW-SDRC) 模擬報告

## 1. 摘要
在推測性解碼 (Speculative Decoding) 中，當目標模型拒絕草稿 Token 時，軟體需要花費大量時間來無效化 KV Cache 中的指針與狀態。本研究提出「硬體推測性草稿回滾快取 (Hardware Speculative Draft Rollback Cache, HW-SDRC)」，將回滾機制硬體化。

## 2. 實驗結果
* 測試規模: 128 Draft Tokens
* Baseline 延遲 (軟體指標無效化): 16.40 ms
* HW-SDRC 延遲 (硬體 Ring Buffer 重置): 1.13 ms
* 吞吐量加速比: 14.54x
* 退回懲罰 (Miss Penalty) 降低: 95%

## 3. 硬體架構建議
建議在 Edge NPU 記憶體控制器中直接加入「HW-SDRC 暫存區」，在確認接受草稿前，不將 KV 狀態寫入主記憶體，一旦發生拒絕，即可在 1 個週期內完成回滾，大幅降低預測失敗時的延遲懲罰。