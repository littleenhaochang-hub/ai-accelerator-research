# Auto-Researcher 實驗報告：Test-Time Compute (o1) 推論分支硬體加速架構
**日期:** 2026-04-13

## 1. 瓶頸分析
根據目前的 `RESEARCH_REPORT.md`，我們關注的另一個瓶頸是 **Test-Time Compute branching** (如 OpenAI o1, R1)。在推理階段進行 Monte Carlo Tree Search (MCTS) 或 Adaptive Branching Tree Search 時，LLM 會在同一個 Prompt 下產生多個平行的 Reasoning Paths (Token 樹枝狀展開)。這會導致 KV Cache 呈現高度的樹狀共享與分支結構，如果硬體加速器與記憶體控制器無法有效處理 Tree-Structured KV Cache 共享，將導致嚴重的記憶體頻寬浪費與冗餘計算。

## 2. 文獻探索
透過檢索 2025/2026 最新 arXiv, ICLR 2025, ICML 2026 論文，我們發現：
*   **Test-Time Compute 趨勢:** 包含 "Forest-of-Thought", "rStar-Math (MCTS)", 與 "Adaptive Branching Tree Search (NeurIPS 2025)"。這些方法將推論計算量大幅拉高以換取準確率。
*   **硬體瓶頸:** 半導體工程研究指出 LLM Inference 的核心挑戰在於記憶體頻寬與互連。Test-Time Scaling (TTS) 使 KV Cache 的存取模式由單一串列變成樹狀 (Tree)，要求硬體支援高效率的 KV Cache 分頁共享 (PagedAttention/RadixAttention 需在硬體層級支援)。
*   **硬體協同設計機會:** 使用 High Bandwidth Flash, Processing-Near-Memory (PNM), 3D memory-logic stacking，並搭配硬體層級的 Tree-Search KV 路由控制器。

## 3. 架構設計 Prototype
在硬體端 (Accelerator Architecture)，我們提出 **Radix-Tree KV Cache Controller (RT-KVC)** 原型概念：
1. **硬體層級的 Prefix Sharing:** 當多個推論分支共享相同的歷史 prompt 或思考前綴時，硬體 DMA 引擎直接將這些 Shared KV Block 映射至同一個 SRAM 地址，避免重複讀取 DRAM。
2. **Copy-on-Write (CoW) for Tokens:** 當分支產生不同 Token 時，才配置新的 KV Block。
3. **MCTS 狀態硬體暫存器:** 在 NPU 中新增特定的暫存器來記錄 Tree Search 的 value scores，減少將狀態寫回 CPU 控制器的延遲。

## 4. 結論
針對 o1 類型的 Test-Time Compute，純粹最佳化 GEMM 是不夠的。我們的 Edge Accelerator 藍圖必須加入支援 Tree-Structured PagedAttention 的硬體控制器，實現 O(1) 的分支切換與 100% 的 Prefix 記憶體共享，以因應未來 MCTS 的推論需求。此報告將併入 `ai-accelerator-research` 的知識庫中。
