# Hardware Fused GEMM & Activation (硬體融合矩陣相乘與激勵函數引擎)

## 實驗背景 (Background)
在 Transformer 的 FFN 層中，傳統流程是 MAC 陣列計算完矩陣相乘 (GEMM) 後，將結果寫回 SRAM。接著，啟動激勵函數 (Activation, 如 SwiGLU) 的 Kernel，重新從 SRAM 讀取數據，計算後再寫回。這種兩階段 (Two-pass) 的做法，浪費了大量的 SRAM 讀寫頻寬與功耗。

## 物理模擬 (Physical Simulation)
透過 `gemm_fused_activation_sim.py`，我們模擬了獨立兩次讀寫與融合架構的延遲差異：
- **標準兩次 Memory Pass 延遲**: 117440.51 ms
- **硬體 In-line 融合延遲**: 85563.80 ms
- **整體加速比**: 1.37x

## 架構提案 (Architectural Proposal)
提議在 Edge NPU 的 Accumulator Register File (累加器暫存器) 輸出端，直接整合 **「Fused Activation LUT & PWL Engine」**。
當 MAC 完成內積運算的瞬間，數值不經過 SRAM，而是直接流經這個硬體激勵函數引擎進行非線性轉換，最後才寫入 SRAM。這種「Zero-DRAM-Bounce」的設計，能減少 FFN 層 50% 的中間暫存讀寫，大幅降低功耗並釋放內部頻寬，非常適合嚴格受限的邊緣裝置。
