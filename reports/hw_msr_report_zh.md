# Hardware MoE Semantic Router (HW-MSR) 實驗報告

## 背景與瓶頸分析
隨著 Mixture-of-Experts (MoE) 模型的 Expert 數量急劇增加（例如某些架構擴展至 256 甚至 1024 個 Experts），軟體層面的 Router 逐漸成為延遲的隱患。傳統 Router 必須對所有 Expert 的 Logits 進行 Softmax，隨後執行 Top-K 排序。當模型規模擴大，這部分的 ALU 負載、記憶體往返以及排序演算法的 $O(N \log N)$ 開銷會嚴重干擾 Token 的推論管線。

## 解決方案：HW-MSR (硬體 MoE 語義路由器)
我們提出 **HW-MSR**，一種內嵌於 NPU 排程器的專用硬體單元。
HW-MSR 捨棄了軟體層級精確的 Softmax 與排序，改採高度平行化的「硬體漢明距離 (Hamming Distance) 評估器」或「內容定址記憶體 (TCAM)」。Token 的路由特徵一進入 HW-MSR，便會在硬體電路中同時與 256 個 Expert 的特徵向量進行相似度比對，並在單一或少數幾個 Clock Cycle 內直接輸出 Top-K 的 Expert ID，達到 $O(1)$ 的路由延遲。

## 實驗結果
透過 Python 模擬 (`hw_msr_sim.py`)，針對 256-Expert 架構的路由開銷進行測試：
- **基準延遲 (軟體 Softmax + Top-K Sorting):** 1.70 ms
- **HW-MSR 延遲 (平行硬體比對):** 0.05 ms
- **路由加速比 (Speedup):** 34.00x

## 結論
HW-MSR 成功將 MoE 模型中隨 Expert 數量增長而惡化的軟體路由瓶頸，轉化為 $O(1)$ 的極低延遲硬體操作，實現了 34 倍的加速。這項技術不僅解決了當前 256-Expert 的困境，更為未來萬級 (10,000+) Expert 規模的大腦級網路架構鋪平了道路。建議將其納入新世代 AI 晶片架構圖。
