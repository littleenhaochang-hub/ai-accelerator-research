# Hardware O(1) Sparse Attention Hash Routing (OSAHR) 模擬實驗報告

## 1. 實驗背景
在處理超長文本 (32K+ Tokens) 時，軟體層級的稀疏注意力機制 (Sparse Attention, 如 LSH 或 Clustering) 會引入 $O(N \log N)$ 甚至更高的路由運算開銷，這抵銷了稀疏化省下來的 MAC 計算時間。

## 2. 實驗方法
我們設計了 `osahr_sparse_attention_sim.py`，驗證在 SRAM 控制器中嵌入硬體級雜湊路由引擎 (OSAHR, O(1) Sparse Attention Hash Router) 的可行性。該硬體能以 $O(1)$ 的延遲找出 Token 所屬的 Attention Bucket，繞過 CPU/NPU 軟體排程器的複雜度。

## 3. 實驗數據與結果
*   **序列長度:** 32768
*   **稀疏度 (Sparsity):** 90%
*   **軟體路由與計算延遲:** 13195.02 ms
*   **硬體 OSAHR 路由與計算延遲:** 10743.97 ms
*   **吞吐量加速比:** 1.23x

## 4. 架構建議
雖然硬體雜湊路由能減少軟體開銷，但對於 90% 稀疏度而言，核心瓶頸仍落在記憶體存取與剩餘的 MAC 運算上。加速比僅 1.23x，顯示單純將路由硬體化的邊際效益有限，建議未來結合「記憶體區塊預取 (Block Prefetching)」與 OSAHR 同步運作，才能進一步打破長文本 Prefill 的效能天花板。