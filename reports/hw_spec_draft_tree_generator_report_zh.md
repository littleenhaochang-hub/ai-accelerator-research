# Hardware Speculative Draft Tree Generator (HW-DTG)

## 實驗背景 (Background)
在推論系統中，Speculative Decoding 需要生成 Draft Token Tree 供主模型驗證。傳統上，這會佔用大量的 SRAM 與 ALU 資源來建立與管理樹狀結構。

## 解決方案 (Proposed Architecture)
我們提出了 **Hardware Draft Tree Generator (HW-DTG)**，將草稿樹的生成與狀態追蹤移至專用的硬體電路中，減少軟體層級的 memory allocation 與 pointer chasing。

## 實驗結果 (Empirical Results)
透過模擬測試：
- **[Baseline] Software Draft Tree Latency:** 58.18 ms
- **[Proposed] HW-DTG Latency:** 37.18 ms
- **Speedup:** 1.56x

## 結論 (Conclusion)
將 HW-DTG 整合進 Edge NPU 的排程器中，能有效加速推測解碼的草稿生成階段。
