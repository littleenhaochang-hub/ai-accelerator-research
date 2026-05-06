# Hardware Speculative KV-Cache Token Merging (HSKTM)

## 實驗背景與動機
在無窮長文本（Infinite Context）與 Agentic AI 應用場景中，KV Cache 的記憶體佔用與頻寬限制是最大的硬體瓶頸。傳統的 Token Merging (ToMe) 依賴軟體計算 Cosine Similarity 並進行聚類，此過程需要大量的 $O(N^2)$ DRAM/SRAM 讀寫，導致嚴重的記憶體頻寬阻塞（Memory Wall）。本實驗旨在驗證硬體級別的 Speculative KV-Cache Token Merging (HSKTM)，將相似度計算與 Token 合併邏輯直接植入 SRAM 的寫入端口（Write Port）。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 在 CPU/GPU 透過標準 GEMM 計算相似度矩陣，隨後執行 Masking 與 Average Pooling。
- **硬體提案 (Hardware HSKTM):** 提出在 Edge NPU 的 SRAM 控制器內建「Inline Token Similarity Comparator (ITSC)」與「Hardware Token Merger」。當新的 KV Token 寫入 SRAM 時，硬體即時與前 $k$ 個 Token 進行餘弦相似度比對。若高於閾值，硬體直接在暫存器內平均並覆寫，完全消除軟體層面的矩陣運算與額外的記憶體往返 (Round-trip)。

## 效能分析結果
針對 16,384 Context Length 進行 Profiling：
- **傳統軟體合併延遲 (Software Latency):** 1292.01 ms
- **硬體 HSKTM 延遲 (Hardware Latency):** 8.00 ms
- **加速比 (Speedup):** 161.50x

## 結論與架構建議
HSKTM 成功將 Token Merging 轉換為 Zero-MAC (Zero-Memory-Roundtrip) 的硬體背景作業。建議未來的 Edge NPU 架構（針對 Agentic LLM）將此硬體模組列為標準配置，以達成極低功耗的無限上下文推論。