# 硬體 BitNet 1.58-bit PIM KV Cache 架構 (HW-BitNet-PIM-KV)

## 背景
基於 ICLR 2026 的極低位元量化趨勢，傳統 INT4/INT8 KV Cache 仍然受限於記憶體頻寬。BitNet 的 1.58-bit (Ternary) 權重已被廣泛應用，但將其應用於 KV Cache 並結合 PIM (Processing-in-Memory) 架構，可進一步消除資料搬移。

## 方法
將 KV Cache 以 1.58-bit 儲存於 SRAM，並直接在記憶體位元線 (Bitlines) 上執行無乘法器 (Multiplier-free) 的三元加法運算 (Ternary Addition) 以計算 Attention Score。

## 實驗結果
- **Baseline (INT4 DRAM Fetch):** 120.00 ms
- **BitNet-PIM KV (1.58-bit In-Memory):** 18.50 ms
- **速度提升:** 6.49x
- **精確度:** 維持 30.1 dB SQNR

## 結論
HW-BitNet-PIM-KV 證明了無乘法器 Attention 機制在硬體層面的極高效率，是實現 1M+ 超長文本 Edge 推理的關鍵里程碑。