# Hardware Prefix Tuning Broadcaster (硬體 Prefix Tuning 廣播引擎)

## 實驗背景 (Background)
Prefix Tuning (連續軟提示微調) 是一種能取代全量微調的高效方法，它會在輸入序列前加上一串可訓練的向量。然而，在支援多使用者的並發伺服器中，軟體 (如 PyTorch) 必須在執行期動態將這些龐大的 Prefix 向量「拼接 (Concatenate)」到每一個使用者的 KV Cache 中。這不僅造成了嚴重的記憶體重複佔用 (Memory Duplication)，其複製的延遲更是拖垮了整體的 Prefill 效能。

## 物理模擬 (Physical Simulation)
透過 `prefix_tuning_hw_sim.py`，比較了軟體動態拼接與硬體 Zero-copy 廣播的延遲差異：
- **軟體動態拼接延遲 (Batch=256, Prefix=1024)**: 107374.18 ms
- **硬體 Zero-copy 廣播延遲**: 5368.71 ms
- **整體加速比**: 20.00x

## 架構提案 (Architectural Proposal)
提議在 NPU 的 Attention ALU 內部整合 **「Hardware Prefix Broadcaster」**。
做法是將訓練好的 Soft-prompt 向量，永久「釘選 (Pin)」在一塊專用的 Shared Prefix SRAM 中。當 NPU 開始運算時，硬體控制器會自動將這些向量「多播 (Multicast)」給 Batch 內的所有 Request，而不需要在記憶體中建立任何副本。這種 Zero-Copy 的設計，徹底解決了多租戶 (Multi-tenant) 推理下 Prefix Tuning 的記憶體暴增與搬移延遲問題。
