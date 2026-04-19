# GaLore On-Device Training 硬體評估報告

## 執行摘要
GaLore (Gradient Low-Rank Projection) 是一種允許進行全參數微調 (Full-parameter fine-tuning)，卻只消耗類似 LoRA 記憶體足跡的技術。它透過將梯度 (Gradient) 投影到低秩子空間 (Low-rank subspace) 來減少 Optimizer 狀態的儲存。本實驗評估 GaLore 應用於 Edge NPU 終端學習 (On-device Learning) 時的硬體瓶頸。

## 實驗數據與分析
- **目標架構**: 7B 模型 (Hidden Dim 4096, 32 Layers), Low-Rank $r=128$
- **記憶體效能評估**:
  - 標準 Adam 狀態容量: 4096.00 MB
  - GaLore Adam 狀態容量: 128.00 MB
  - 記憶體縮減比率: 32.00x (節省 96.8%)
- **算力瓶頸 (SVD Overhead)**:
  - 進行單次 SVD 的算力: 6.87e+10 FLOPs
  - 單個 Token 的 FW+BW 算力: 1.01e+08 FLOPs
  - SVD 的計算量相當於一次處理 **682 個 Tokens**。

## 硬體架構結論
1. **解除記憶體封印**: GaLore 成功將 Edge 端的 Optimizer 記憶體需求從 4GB 壓縮至 128MB，使得終端裝置 (如手機、PC) 能執行 LLM 個人化學習。
2. **極端的算力失衡**: SVD (奇異值分解) 的 $O(N^3)$ 複雜度，在沒有硬體加速的情況下，會導致訓練過程中出現嚴重的停頓 (Stalls)。
3. **協同設計提案**: 若 Edge NPU 要支援終端全參數微調，必須內建「Asynchronous Randomized SVD Engine (非同步隨機奇異值分解引擎)」。利用 NPU 的閒置週期，在背景非同步地運算投影矩陣，或採用近似低秩分解硬體，以掩蓋長達數百個 Token 週期的 SVD 延遲。
