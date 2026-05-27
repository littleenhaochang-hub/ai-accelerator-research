# Hardware MoE Sub-Token Routing (HW-MSTR)

## 概述
為了解決 MoE 架構中，必須等待 Token Embedding 與早期 Transformer 層計算完畢後才能進行路由（Routing）並觸發 PCIe 專家權重拉取的延遲問題，本研究提出 Hardware MoE Sub-Token Routing (HW-MSTR)。

## 實驗方法
HW-MSTR 在 NPU 的 Ingress 控制器中整合了一個硬體字串匹配器 (Hardware String Matcher)。該引擎在 Byte/Sub-word 階段即可根據歷史字首與特徵，預測該 Token 最終將被送往的 MoE 專家，並提前啟動非同步 DMA 預取。

## 實驗數據
*   **基準拉取延遲 (Baseline):** 15.62 ms (Batch Size 256)
*   **子詞預測命中率:** 88.0%
*   **HW-MSTR 延遲:** 1.89 ms
*   **整體延遲加速比 (Speedup):** 8.26x

## 結論與架構建議
藉由將 MoE 路由決策從高層語義空間（隱藏狀態向量）下放到低層詞彙空間（Sub-token 字串匹配），我們能爭取到最長的前置時間來掩蓋 PCIe 延遲。建議未來的 Edge NPU 在前端直接內建此類 Sub-token 預測器，以支援超大參數量的 Agentic MoE 模型。
