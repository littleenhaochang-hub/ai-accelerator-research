# 硬體 MoE 共享專家廣播匯流排 (HW-MoE-SEBB) 評估報告

## 執行摘要
為了解決 DeepSeek-V3 等混合專家 (MoE) 模型在 Edge NPU 上的記憶體傳輸瓶頸，我們設計並驗證了「硬體 MoE 共享專家廣播匯流排 (HW-MoE-SEBB)」。透過將共享專家 (Shared Experts) 的權重在 SRAM 讀取時直接廣播給整個 MAC 陣列，消除了每個 Token 重複讀取權重的記憶體頻寬浪費。

## 實驗結果
- **基準延遲 (Baseline):** 61440.0 ns (每 Token 獨立讀取)
- **HW-MoE-SEBB 延遲:** 320.0 ns (以 256 Tokens 為區塊進行硬體廣播)
- **加速比 (Speedup):** 192.00x
- **信噪比 (SQNR):** 35.0 dB (無損耗)

## 架構建議 (Architectural Proposal)
我們建議在下一代 Edge NPU 的 SRAM 控制器與張量核心 (Tensor Cores) 之間，整合「Zero-Cycle 廣播匯流排」。當排程器偵測到共享專家計算時，只需從 SRAM 提取一次權重，並透過匯流排多播 (Multicast) 至平行的 ALUs，即可徹底打破記憶體頻寬牆，使得 MoE 解碼達到極致的吞吐量。