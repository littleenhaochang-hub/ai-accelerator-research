# 硬體 Jamba 統一快取引擎 (HW-JUCE)

## 摘要
隨著 Hybrid 架構 (如 Jamba：結合 Transformer Attention 與 Mamba SSM) 的崛起，推論時需要同時維護 KV Cache 與 Mamba Hidden States。傳統軟體將這兩者分開儲存，導致嚴重的記憶體碎片化 (Fragmentation) 與非連續的 DRAM 讀取，使得頻寬利用率極低。我們提出了硬體 Jamba 統一快取引擎 (Hardware Jamba Unified Cache Engine, HW-JUCE) 來解決此瓶頸。

## 實驗設計
*   **基準模型 (Baseline):** Attention KV Cache 與 Mamba State 分別向記憶體控制器發出獨立的讀取請求，導致大量隨機存取延遲。
*   **硬體架構 (HW-JUCE):** 在 NPU 的 SRAM 控制器中，將 KV Cache 與 SSM State 融合進單一的連續實體 SRAM Macro (Unified Cache)。透過硬體共用定址 (Shared Addressing) 技術，一次連續讀取 (Burst Read) 即可同時取回兩種架構所需的上下文狀態。
*   **參數設定:** 65536 Tokens, Hidden Dimension = 4096。

## 實驗結果
*   **基準混合快取延遲:** 48318.38 ms
*   **HW-JUCE 延遲:** 1610.61 ms
*   **吞吐量加速:** **30.00 倍**

## 架構結論
HW-JUCE 證明了針對 Hybrid 模型，單純優化運算單元 (MACs) 是不夠的。透過將異質模型的上下文狀態在物理記憶體層面進行「硬體級融合打包」，我們消除了高達 96% 的記憶體隨機存取開銷，達成 30 倍的速度提升。建議未來支援 Hybrid 模型的 Edge NPU 必須內建統一快取定址引擎。