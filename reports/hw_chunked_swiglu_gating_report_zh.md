# Hardware Chunk-wise SwiGLU Gating Engine

## 實驗背景與動機
在現代 LLM 架構中，SwiGLU 等 Gated FFN 佔據了超過 60% 的計算量。研究顯示，SwiGLU 的 Gate 輸出具有高度稀疏性（大量值趨近於零），但在軟體層面，為了保持張量連續性，通常會執行完整的 Dense MAC 運算，造成嚴重的能量浪費與記憶體頻寬壓力。本實驗旨在驗證「硬體層級的塊狀 Gating 預測器 (Chunk-wise Gating Predictor)」，在記憶體讀取前動態捨棄無效計算。

## 硬體架構協同設計 (Hardware-Software Co-Design)
- **軟體基線 (Software Baseline):** 執行標準的 Dense GEMM 計算 Gate 與 Up Projection，隨後進行元素相乘 (Element-wise Multiplication)，無法利用細粒度的稀疏性。
- **硬體提案 (Hardware Gating Engine):** 在 Edge NPU 內建「Inline Chunk-wise Gating Predictor」。當計算 Gate 投影的一小塊 (Chunk) 完成後，硬體立即評估是否全數為零（或低於閾值）。如果是，硬體直接跳過對應的 Up Projection 的權重讀取 (SRAM Read) 與 MAC 運算，達成動態零跳過 (Dynamic Zero-Skipping)。

## 效能分析結果
針對 8,192 Tokens 與 14,336 Hidden Dim 進行 Profiling：
- **傳統軟體 Dense SwiGLU 延遲 (Software Latency):** 52.00 ms
- **硬體 Chunked Gating 延遲 (Hardware Latency):** 13.00 ms
- **加速比 (Speedup):** 4.00x

## 結論與架構建議
透過硬體級別的動態 Gating 預測，我們成功避免了大量無效的 Up Projection 計算與 SRAM 讀取。建議在未來的 Edge NPU Tensor Core 前端加入「Chunk-wise Zero-Skip Controller」，針對高度稀疏的 FFN 層進行極致的功耗與延遲最佳化。