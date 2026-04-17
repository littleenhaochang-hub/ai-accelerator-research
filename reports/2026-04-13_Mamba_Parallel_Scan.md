# Auto-Researcher 實驗報告：Mamba/RetNet Parallel Scans 最佳化
**日期:** 2026-04-13

## 1. 瓶頸分析
根據 `RESEARCH_REPORT.md`，Transformer 架構的 $O(N^2)$ 注意力機制導致長文本 (Prefill) 處理緩慢且佔用過多 KV Cache。Mamba 與 RetNet (State Space Models, SSMs) 具備 $O(N)$ 線性複雜度，但在硬體層級上，傳統的依序 (Sequential) 處理模式導致硬體平行度 (GPU/NPU utilization) 低下。

## 2. 文獻探索
從 arXiv 2025/2026 以及 ICML/ICLR 的最新研究中，我們發現：
*   **Mamba硬體加速器:** 如 LightMamba, FastMamba, Mamba-X (ICCAD 2025) 專注於 FPGA 或邊緣設備加速。
*   **Parallel Scan Algorithms:** 論文提出了 "Matrix-engine (Tensor Core) scan"，將 prefix-sum (scan) 電路推廣到 Tensor Core 上，利用矩陣乘法加速。
*   **Kogge-Stone Tree:** Mamba-X 採用基於 Kogge-Stone 演算法的 Systolic Scan Array (SSA) 來最大化選擇性掃描 (selective scan) 的平行度。

## 3. Prototype 驗證
我們編寫 `mamba_scan_prototype.py` 模擬了長度 $L=4096$ 的 Prefix Scan。
*   傳統 RNN 循序處理需要 $O(L) = 4096$ 個時間步。
*   採用 Kogge-Stone Matrix Scan，深度降為 $O(\log L) = 12$ 個時間步。
*   即使考慮 Tensor Core 的額外單步延遲，**整體理論加速比高達 136.53x**。

## 4. 結論
針對邊緣運算 (Edge AI)，我們未來設計 AI Accelerator 時，不應只堆疊傳統的 GEMM 乘加器 (MACs)，而應引入 **Systolic Scan Array (SSA) 或支援 Matrix-based Scan 的特殊 Tensor Core 單元**。這能徹底解放 Mamba/RetNet 模型在硬體上的平行潛力，達成超高速、低功耗的 Prefill 階段。
