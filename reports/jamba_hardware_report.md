# Jamba (MoE-Mamba Hybrid) 硬體架構分析報告

## 1. 實驗動機 (Motivation)
隨著模型架構朝向 MoE 與 SSM (State Space Models, 如 Mamba) 的混合體 (例如 Jamba) 發展，雖然能有效解決長文本 (Long Context) 下的 KV Cache 容量問題，但硬體層面仍面臨兩大瓶頸：
1. **MoE 專家權重提取 (Expert Fetching)：** DRAM 到 SRAM 的龐大頻寬需求。
2. **Mamba 狀態更新序列依賴 (Sequential Scan)：** 使得純矩陣運算的張量核心 (Tensor Cores) 利用率低落。

## 2. 硬體-軟體協同設計提案 (Hardware-Software Co-Design)
為了解決此瓶頸，我們提出 **「非同步 Jamba DMA 與平行掃描排程器 (Asynchronous Jamba DMA & Scan Scheduler)」**：
*   在硬體 DMA 控制器中加入「前瞻提取 (Lookahead Prefetching)」，當 NPU 正在計算第 N 層的 Mamba Block 時，背景非同步將第 N+1 層的 MoE Expert 權重從 DRAM 搬移至 SRAM。
*   將 Mamba 的線性掃描改用「關聯掃描 ALU 樹 (Associative Scan ALU Trees)」進行平行化加速。

## 3. PyTorch 原型模擬結果 (Simulation Results)
透過 `jamba_hardware_sim.py` 的微架構時序模擬：
*   **基準測試 (Baseline)：** 同步 Fetch 與 Sequential Scan，單次 Inference 耗時約 1022.41 ms。
*   **非同步重疊 (Proposed)：** 將 Fetch 隱藏於 Compute 之後，並加速 Scan，耗時降至 367.58 ms。
*   **效能提升：** 整體吞吐量達到 **2.78x Speedup**。

## 4. 結論與邊緣 NPU 整合建議 (Conclusion)
實驗證明，若要在 Edge NPU (如 Mac mini 或移動終端) 上高效運行 Jamba 這類混合架構，純軟體優化是不夠的。我們強烈建議在下一代邊緣 NPU 架構中，將 DMA 控制器與關聯掃描 ALU 直接做硬體級別的 Pipeline 綁定，以實現 100% 的 Compute-bound 執行。
