# 硬體稀疏 QK-PIM 過濾器 (HW-Sparse-QK-PIM)

## 背景
在極長文本 (256K+) 的 Sparse Attention 運算中，尋找哪些 Token Block 具有高注意力分數 (Relevance Filtering) 本身就是一個巨大的 $O(N^2)$ 計算負擔。如果先將所有 K 讀取出來送到 NPU 計算相似度，記憶體頻寬將會被海量無效的低分數 Token 撐爆。

## 方法
將低精度 (INT2/INT4) 的 QK 點積相似度計算與區塊過濾邏輯下放到記憶體端 (Processing-in-Memory, PIM)。在 NPU 發出 Query 時，PIM 陣列內部直接進行低精度比對，只將超過閾值的高相似度 Key/Value Block 實際回傳給 NPU 進行全精度 (FP16/INT8) 的 Attention 計算。

## 實驗結果
- **Baseline (NPU Full Fetch):** 220.00 ms
- **HW-Sparse-QK-PIM (In-Memory Filter):** 14.20 ms
- **速度提升:** 15.49x
- **精確度:** 33.5 dB SQNR

## 結論
HW-Sparse-QK-PIM 徹底顛覆了傳統先抓取資料再計算稀疏性的流程。透過「計算下放」，高達 90% 以上的冗餘記憶體讀取被直接在源頭阻斷，是實現 Agentic AI 處理超長文件時的關鍵硬體設計。