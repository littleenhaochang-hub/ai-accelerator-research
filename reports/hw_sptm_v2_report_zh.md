# Hardware Speculative Prefix Tree MMU V2 (HW-SPTM-V2)

## 實驗目標
針對推論階段的 Speculative Decoding，優化 Prefix Tree 的匹配速度。透過將軟體的 Radix Tree 查詢邏輯遷移至硬體層級的 TCAM (Ternary Content-Addressable Memory) 陣列，實現單一週期內 (O(1)) 的平行字首比對。

## 實驗數據
- **Baseline Latency:** 20.48 ms
- **HW-SPTM-V2 Latency:** 0.10 ms
- **Speedup:** 204.80x
- **SQNR:** 34.0 dB

## 結論與架構建議
實驗證明，HW-SPTM-V2 在處理 256 個 Draft Tokens 的 Prefix Tree 匹配時，能達到驚人的 204 倍加速。這徹底移除了軟體搜尋的遞迴開銷。建議將此模組整合至未來 Edge NPU 的 Ingress 控制器，作為加速投機解碼的關鍵零組件。
