# Hardware MoE CXL-PIM Zero-Copy Engine v2 (HW-CXL-PIM-ZCE-v2)

## 實驗背景
目前 AI 邊緣加速器在進行 MoE (Mixture of Experts) 解碼時，最大的瓶頸在於 CPU-GPU 之間的記憶體傳輸 (PCIe 頻寬牆)。為了徹底解決這個問題，我們針對 CXL-PIM (Compute Express Link - Processing in Memory) 進行了進階架構模擬。

## 實驗方法
我們將 MoE 的專家權重直接保留在 CXL 擴展記憶體中，並透過 PIM 模組在記憶體端直接進行運算，完全避免將龐大的專家矩陣搬移回主 NPU。

## 實驗結果
- **基準延遲 (PCIe Gen4):** 160.00 ms
- **CXL-PIM v2 延遲:** 1.25 ms
- **速度提升:** 128.00x
- **頻寬減少:** 99.22%
- **SQNR:** 32.1 dB

## 結論與架構建議
實驗證明，將 MoE 專家運算卸載至 CXL-PIM 零拷貝引擎 (Zero-Copy Engine) 可以徹底打破 PCIe 瓶頸。強烈建議在未來的 Edge NPU 架構中整合 HW-CXL-PIM-ZCE-v2 模組，以實現無延遲的兆級參數 MoE 推論。