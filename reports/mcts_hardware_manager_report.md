# Test-Time Compute: MCTS 硬體樹狀管理器分析報告

## 瓶頸分析
根據 `RESEARCH_REPORT.md`，在為 LLM (如 DeepSeek R1 / OpenAI o1) 執行 Test-Time Compute (System 2 思考) 時，常採用蒙地卡羅樹狀搜尋 (MCTS)。若由 CPU 負責維護搜尋樹的狀態 (如 UCB 分數計算、節點擴展)，並透過 PCIe 將狀態傳送給 NPU 進行 Rollout 評估，會產生嚴重的 PCIe 延遲與 NPU 閒置 (Bubble)。

## 解決方案：NPU 內建硬體 MCTS 管理器 (Hardware MCTS Manager)
我們提出將 MCTS 的樹狀結構直接 mapping 到 NPU 的 SRAM 中，並加入專用的「硬體 UCB 計算單元」與「節點指標管理器」。這使得 NPU 能夠自主進行樹狀展開與探索，完全無需與 CPU 進行 PCIe 同步，直到最終決策產出。

## 實驗結果
透過 Python 模擬 `mcts_hardware_manager_sim.py` (展開 2048 個節點)：
- **CPU MCTS 總延遲:** 3891.20 ms
- **硬體 MCTS 總延遲:** 3112.96 ms
- **加速比:** 1.25x

*(註：雖然絕對延遲降低 25%，但更大的效益在於釋放了 CPU 資源並去除了 PCIe 頻寬佔用，讓 NPU 可以進行更大規模的平行 Rollout)*

## 結論
將搜尋樹硬體化能有效減少 Test-Time Compute 的通訊開銷。建議未來的 AI 加速器在排程器旁增設「Hardware Tree Manager」，以原生支援推論期的強化學習與搜尋演算法。
