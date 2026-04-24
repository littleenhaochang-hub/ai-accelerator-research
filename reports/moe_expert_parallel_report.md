# MoE Expert Parallelism 晶片內平行化報告

## 瓶頸分析
傳統的 NPU/GPU 架構通常配備單一龐大的 Tensor Core 陣列。當執行 MoE 模型時，Router 將 Token 分配給不同 Expert 後，這個巨大的陣列必須「循序」切換不同的 Expert 權重來處理對應的 Token。這造成嚴重的權重載入延遲與運算氣泡。

## 解決方案：晶片內多核心 Expert 平行化 (On-Die Expert Parallelism)
我們提出將單一龐大的 MAC 陣列拆分為多個較小、獨立的「子核心 (Sub-Cores)」。當 Token 分發後，這些子核心可以「同時」載入不同的 Expert 權重並平行計算。

## 實驗結果
透過 Python 模擬 `moe_expert_parallel_sim.py`：
- **循序 Expert 計算 (單一大核心):** 17,179,869,184 單位延遲
- **平行 Expert 計算 (多個子核心):** 2,147,483,648 單位延遲
- **加速比:** 8.00x

## 結論
硬體層級的 Sub-Core 拆分能讓 MoE 模型達到真正的平行化，延遲縮減與拆分的 Expert 數量成正比。建議未來的 Edge NPU 從「單一巨核」轉向「多小核 (Multi-Tile)」架構。
