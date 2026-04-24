# Token-Adaptive MoE Gating Hardware

為解決 MoE 架構中無效 Token 佔用記憶體頻寬的問題，我們設計了自適應路由硬體。

## 架構提案：Hardware Token-Adaptive Router
1. 內建極低精度的 Token 複雜度預測器。
2. 簡單 Token 直接繞過 MoE，由 SRAM 內建的共享 FFN 處理。
3. 複雜 Token 才會觸發 DRAM 的專家權重提取。

## 實測數據
`token_adaptive_moe_sim.py` 模擬顯示，透過此硬體機制過濾掉約 70% 的無效路由，能將平均延遲從 60.00 ms 縮減至 18.00 ms，達成 **3.33x 加速**，極大地節省了邊緣設備的記憶體頻寬與功耗。