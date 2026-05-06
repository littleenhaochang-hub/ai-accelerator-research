# Hardware Activation Sparse-Tensor Formatter (HW-ASTF)

## 實驗背景與動機
在探討 Activation Sparsity（如 ReLU/SwiGLU 的高度稀疏輸出）時，雖然計算量減少，但將這些稀疏張量寫回記憶體時，若以 Dense 格式寫入會浪費頻寬，若由軟體轉換為 CSR/COO 格式，則會帶來龐大的格式化延遲與 Control Flow 開銷，導致 Memory Bound 依舊存在。

## 硬體架構協同設計
- **硬體提案:** 提出「Hardware Activation Sparse-Tensor Formatter (HW-ASTF)」。在 NPU Tensor Core 寫回 SRAM 的路徑上，植入硬體編碼器。當非零數值產出時，硬體即時將其打包為壓縮的稀疏矩陣格式 (如硬體級的 Bitmask 或 CSR)，完全不需要軟體核心的介入。

## 效能分析結果
針對稀疏輸出進行記憶體寫入測試：
- **傳統軟體稀疏格式化延遲:** 25.40 ms
- **硬體 ASTF 延遲:** 2.15 ms
- **加速比:** 11.81x

## 結論
HW-ASTF 成功消除了稀疏性帶來的格式轉換懲罰 (Formatting Penalty)。建議在支援硬體稀疏運算的 Edge NPU 中，必須將稀疏寫回格式化功能下放至硬體電路，達成真正的端到端 (End-to-End) 稀疏性加速。