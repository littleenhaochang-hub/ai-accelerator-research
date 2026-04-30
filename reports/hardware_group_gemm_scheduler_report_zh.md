# Hardware Group-GEMM Command Scheduler 實驗報告

## 1. 實驗背景
在 MoE 模型或多 Batch 處理中，經常需要執行 Group-GEMM (多組不同大小的矩陣乘法並行)。傳統軟體需要透過 CPU 或驅動程式發送多個獨立的 Kernel Launch 指令，這些 Launch Overhead 在極端的 Edge 裝置上會吃掉大量的 TPS。

## 2. 實驗方法
設計 `hardware_group_gemm_scheduler_sim.py`，模擬一個硬體層級的 Group-GEMM 指令排程器。CPU 只需發送單一「Group-GEMM 巨集指令」，硬體排程器會自動在 NPU 內部將其展開 (Unroll)，並動態分配給不同的 MAC 陣列執行。

## 3. 實驗數據與結果
*   **Layers:** 64
*   **Batch Size:** 128
*   **軟體 Launch 延遲:** 40.96 ms
*   **硬體排程器延遲:** 0.82 ms
*   **加速比:** 50.00x

## 4. 架構建議
為了榨乾 Edge NPU 算術單元的極限效能，必須盡可能減少 CPU 的控制介入。建議在下一代 Tape-out 中整合「Hardware Group-GEMM Scheduler」，以單一指令觸發複雜的多張量並行運算，消除軟體排程帶來的 Pipeline Bubble。