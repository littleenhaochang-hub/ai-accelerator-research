# Hardware Prefix Cache Tree Walker 模擬報告

## 摘要
本報告探討將 Prefix Caching (如 Radix Tree) 的檢索過程從 CPU 軟體轉移至 Edge NPU 內的專屬硬體單元 (Hardware Tree Walker)。

## 實驗設計
- 測試 64K token 的 Prompt Cache 匹配。
- 軟體延遲基於 CPU 記憶體指標跳轉；硬體延遲基於專屬 MMU 加速。

## 實驗結果
- **SW Latency**: 320.0 s
- **HW Latency**: 6.4 s
- **Speedup**: 50.00x

## 架構建議
硬體樹狀走訪器 (Hardware Tree Walker) 可將多輪對話的 Prefix 匹配延遲縮減 50 倍，建議將其整合進 Agentic AI 專用 NPU 的記憶體控制器中。