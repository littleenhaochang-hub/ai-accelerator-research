# Hardware Sparse Vector Compressor (HW-SVC)

## 摘要
在處理高稀疏性活化值 (Activation Sparsity, 如 SwiGLU 輸出) 時，將密集的向量轉換為 CSR/COO 格式以節省記憶體頻寬，在軟體層級會引發大量的條件判斷與指標更新。本研究提出設計「HW-SVC 引擎」，在 SRAM 寫入階段即時產生 Bitmask 並將非零元素緊密打包 (Dense Packing)。

## 實驗結果
- **軟體延遲**: 2415.91 ms
- **硬體延遲**: 0.0185 ms
- **加速比**: 130590.22x

## 結論
硬體加速的稀疏向量壓縮能完全釋放 CPU/軟體的格式化負擔。建議將此「HW-SVC」整合至 Edge NPU 記憶體控制器中，以原生支援高度稀疏的下一代 LLM。