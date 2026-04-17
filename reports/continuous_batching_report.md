# Continuous Batching Hardware Scheduling Report
## 背景 (Background)
傳統 Static Batching 會因為 Batch 中序列長度不一，導致提早結束的 Request 佔用硬體氣泡 (Padding Bubbles)，嚴重浪費 MAC 單元的吞吐量。Continuous Batching (如 Orca) 能在 token-level 動態抽換 Request。

## 模擬參數 (Parameters)
- Total Requests: 100
- Batch Size: 16
- Sequence Lengths: Uniform(100, 1000)

## 模擬結果 (Results)
- Static Batching 週期: 6436.00
- Continuous Batching 週期: 3293.44
- 系統吞吐量提升: 1.95x

## 架構建議 (Architectural Proposal)
為了完全釋放 Continuous Batching 的效能，Edge NPU 必須配備 **Hardware Context Switcher** 與 **Fine-grained Token Scheduler**。這允許 NPU 的排程器在硬體層級 (Cycle-level) 即時將已完成的 Token Slot 替換為等待佇列中的新 Request Token，確保 MAC Array 的利用率 (Utilization) 永遠維持在接近 100%。
