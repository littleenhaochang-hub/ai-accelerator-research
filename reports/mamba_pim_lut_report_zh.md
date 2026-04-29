# Mamba PIM + LUT 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
Mamba/SSM 模型在推論時，State 狀態更新頻繁導致記憶體頻寬成為瓶頸 (Memory Wall)。

## 2. 探索文獻 (Explore)
結合 Processing-in-Memory (PIM) 與 Look-Up Table (LUT) 技術。

## 3. 建立原型並驗證 (Prototype & Test)
執行 `mamba_pim_lut_sim.py`，取得 **12.50x** 延遲加速。

## 4. 架構結論與建議
建議在 Edge NPU 記憶體控制器中實作 PIM+LUT，實現零延遲 Mamba 狀態更新。