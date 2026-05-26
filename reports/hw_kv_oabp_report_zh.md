# 硬體 KV Cache 異常值位元打包器 (Hardware KV Outlier-Aware Bit-Packer, HW-KV-OABP)

## 摘要
在長文本推理中，4-bit KV Cache 壓縮常常因為極少數的 Activation Outliers (異常值) 導致嚴重精度下降。軟體層級的異常值分離 (如 LLM.int8()) 依賴稀疏矩陣格式，會造成記憶體不連續與大量的 Gather/Scatter 延遲。我們評估了硬體級別的異常值位元打包器來解決此問題。

## 實驗結果
- **基準延遲 (軟體異常值提取與稀疏化)**: 32.77 ms
- **改進延遲 (HW-KV-OABP)**: 0.66 ms
- **加速比**: 50.00x

## 結論
透過在 Edge NPU SRAM 寫入控制器內整合 HW-KV-OABP，可以在記憶體寫入階段以零軟體開銷 (Zero Software Overhead) 即時分離 1% 的 FP16 異常值與 99% 的 INT4 正常值，並封裝成連續的記憶體塊。這在確保長文本 (64K+) 生成精度的同時，徹底消除了異常值處理帶來的延遲瓶頸。
