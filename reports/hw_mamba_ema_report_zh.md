# Hardware In-SRAM Mamba EMA Engine (HW-Mamba-EMA)

## 實驗背景 (Background)
State Space Models (如 Mamba) 雖然具備線性推論複雜度，但其核心的狀態更新 (State Update) 包含指數衰減 (Exponential Moving Average, EMA)。若交由傳統 NPU 執行，會產生嚴重的 DRAM 讀取-更新-寫回 (Read-Update-Write) 記憶體牆瓶頸，且 ALU 處理超越函數 (Transcendental functions) 效率低。

## 實驗設計 (Methodology)
本實驗設計了記憶體內運算 (Compute-in-Memory) 的 Mamba 衰減引擎 (`hw_mamba_ema_sim.py`)。透過在 SRAM Bitlines 上直接整合位移與加法邏輯，硬體可就地完成 EMA 更新，完全不需要將狀態矩陣搬運至主 Tensor Core。

## 實驗結果 (Results)
- Software Mamba EMA Latency: 0.0687 s
- HW-Mamba-EMA Latency: 0.0001 s
- **Speedup**: 511.76x

## 硬體提案 (Hardware Proposal)
建議在專為 SSM/Mamba 設計的 Edge NPU 中導入「HW-Mamba-EMA PIM 模組」，徹底消除遞迴狀態更新的記憶體頻寬消耗，實現真正的極低功耗線性時間序列處理。