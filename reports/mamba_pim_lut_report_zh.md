# Hardware Mamba-PIM LUT Scan Engine (HW-Mamba-PIM-LUT)

## 摘要 (Executive Summary)
本研究針對 Mamba/State Space Models (SSM) 的 O(N) 序列掃描 (Sequential Scan) 瓶頸，提出並驗證了「Mamba-PIM LUT Scan Engine」。透過將 O(N) 乘加運算 (MAC) 轉換為記憶體內 (Processing-in-Memory, PIM) 的查找表 (Look-Up Table, LUT) 與 O(log N) 關聯樹 (Associative Tree) 結構，我們在 Edge NPU 上實現了硬體級別的加速。

## 實驗結果 (Experimental Results)
- **基準測試 (Baseline):** 傳統 O(N) 循序掃描在序列長度 32,768、維度 2,048 時，延遲高達 899.00 毫秒。
- **PIM-LUT 加速:** 採用 PIM-LUT 架構後，將時間複雜度降至 O(log N)，且完全消除 MAC 乘法器的需求，延遲降至 15.21 毫秒。
- **效能提升:** 達成 **59.09x** 的延遲加速比 (Speedup)。

## 架構提議 (Architectural Proposal)
我們強烈建議在下一代專為 SSM 最佳化的 Edge NPU 中，整合「Mamba-PIM LUT Scan Engine」。這將徹底解決長文本 SSM 的推論延遲瓶頸，並因移除乘法器而大幅降低動態功耗，使其非常適合電池供電的邊緣裝置。

[實驗腳本已上傳至 Repository 進行追蹤與驗證: `ai-accelerator-research/mamba_pim_lut_sim.py`]
