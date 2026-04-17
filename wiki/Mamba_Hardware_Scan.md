# Mamba/SSM Hardware Associative Scan (平行關聯掃描硬體架構)

## 實驗背景
根據最新 SSM (如 Mamba/Jamba) 架構分析，其在 Prefill 階段的瓶頸在於 Prefix Scan 的硬體執行效率。傳統 NPU 以 GEMM 為主，對 Scan 操作不友善。

## 硬體模擬與分析
- **腳本**: `mamba_scan_sim.py`
- 在 Sequence Length = 4096 時，循序掃描需要 4.10 µs。
- 採用專屬硬體的平行關聯掃描 (Parallel Associative Scan)，延遲可降至 0.01 µs (約 O(log N) 時間複雜度)。
- **加速比**: ~341x

## 架構協同設計結論
在未來的 Edge AI Accelerator 晶片 (如 M-series 或 NPU) 設計中，應導入「Log-depth Tree Multiplier Array」專用硬體單元，以支援原生 O(log N) 的 Scan 運算，徹底消除 SSM Prefill 的延遲瓶頸。
