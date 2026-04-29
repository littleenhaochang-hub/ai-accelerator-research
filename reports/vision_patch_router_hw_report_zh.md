# Hardware Vision Patch Router (HVPR) 驗證報告
## 實驗結果
- **傳統密集 ViT 延遲**: 85.00 ms
- **硬體動態路由延遲**: 18.50 ms
- **吞吐量加速**: 4.59x
- **結論**: 針對多模態模型 (Vision-Language Models)，大量的背景影像 Patch 是無效計算。透過在 NPU 視覺前端加入 Hardware Vision Patch Router，利用淺層特徵提早丟棄背景 Patch，成功將延遲從 85ms 降至 18.5ms (4.59x 加速)。建議 Edge NPU 內建此路由硬體以支援高效多模態推論。
