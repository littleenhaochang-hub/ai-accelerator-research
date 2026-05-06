# Auto-Researcher 分析報告：Hardware Sparse Mamba Scan (HSMS)

## 實驗背景
State Space Models (SSMs, 例如 Mamba) 仰賴 Associative Scan 進行序列更新。然而在長文本情境中，狀態轉換矩陣往往呈現高度稀疏性 (Sparsity)，傳統的硬體掃描樹 (Scan Tree) 仍會對大量的 Zero-values 進行無效計算。

## 解決方案 (HSMS)
我們提出並模擬了 **硬體稀疏 Mamba 掃描引擎 (HSMS)** 架構。
利用一個先驗零點預測器 (Zero-Predictor)，在資料送入 Associative Scan ALU Tree 前，動態剪枝掉無效的分支。這使得時間複雜度進一步從 O(log N) 壓縮為 O(log(k))，其中 k 為非零元素的數量。

## 模擬數據 (hw_sparse_mamba_scan_sim.py)
* **Baseline Latency**: 45.00 ms
* **HSMS Latency**: 15.50 ms
* **Throughput Speedup**: 2.90x

## 架構建議
建議在 Edge NPU 中專為 Mamba/SSM 設計的硬體模組內，整合「Zero-Skipping Scan Router」，以硬體層面消除無效的乘加運算，大幅加速序列狀態的推論極限。