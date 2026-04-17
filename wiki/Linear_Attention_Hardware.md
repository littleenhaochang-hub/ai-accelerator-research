# Linear Attention Hardware Architecture

## 實驗背景
對於極長文本 (>16K)，標準 Attention 的 $O(N^2)$ 複雜度會使得推論完全卡在 MAC 運算和記憶體頻寬。Linear Attention 透過結合律將運算順序改為 $O(N)$。

## 硬體模擬與分析
- **腳本**: `linear_attention_sim.py`
- 在 16K Context 下，Linear Attention 將 MACs 從 343 億次驟降至 1.34 億次。
- 達成驚人的 **256.00x** 硬體加速比。

## 架構協同設計結論
Edge NPU 的設計重心必須從「處理巨大 N 維度矩陣」轉向「極速更新 D 維度狀態」。建議在硬體架構中導入 **KV State Accumulator Array**，專注於 Head Dimension (D) 大小的狀態矩陣更新，完全消除傳統 Softmax 導致的 Pipeline 停滯。
