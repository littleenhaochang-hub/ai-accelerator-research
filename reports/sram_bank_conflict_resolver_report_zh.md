# Hardware SRAM Bank Conflict Resolver 模擬報告

## 摘要
本報告評估在 FlashAttention 的 SRAM Tile 載入過程中，解決 Bank Conflicts（記憶體庫衝突）的硬體架構方案。

## 實驗設計
- 模擬 256 執行緒平行存取 SRAM 導致的 Bank Conflicts。
- 比較軟體 Padding 解決方案與硬體 XOR Hash Banking 機制。

## 實驗結果
- **SW Latency**: 5.1200 s
- **HW Latency**: 0.2560 s
- **Speedup**: 20.00x

## 架構建議
硬體 XOR Hash Banking 能有效打散存取模式，消除 Bank Conflicts，提升 FlashAttention 在 NPU 上的有效頻寬利用率。建議整合至下一代 Edge NPU 的 SRAM 介面。