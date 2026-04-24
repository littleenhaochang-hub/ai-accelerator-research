# Hardware Micro-Pipeline Parallelism (硬體微管線平行處理)

## 實驗背景 (Background)
在模型自迴歸解碼 (Decoding) 階段，傳統軟體框架 (如 PyTorch) 都是採取「Layer-by-Layer」的執行方式。即便引入了 Continuous Batching，同一個 Batch 內的 Token 仍然必須等待彼此算完第 $L$ 層，才能集體進入第 $L+1$ 層。這產生了巨大的管線氣泡 (Pipeline Bubbles)，導致 Token 生成延遲 (TBT) 居高不下。

## 物理模擬 (Physical Simulation)
透過 `micro_pipeline_hw_sim.py`，比較了傳統按層同步執行與硬體微管線 (Micro-Pipeline) 的延遲：
- **傳統 Layer-by-Layer 延遲 (模擬 1000 Tokens, 32 Layers)**: 325.00 ms
- **硬體非同步微管線延遲**: 10.32 ms
- **整體加速比**: 31.49x

## 架構提案 (Architectural Proposal)
提議將 Edge NPU 的排程器升級為 **「Asynchronous Token Micro-Pipeline Controller」**。
徹底打破「按層同步」的限制。當某個 Token 在第 $L$ 層計算完畢後，硬體會直接將其狀態向量推入第 $L+1$ 層的輸入佇列，無須等待 Batch 內的其他 Token。這種非同步的流水線設計，能將解碼階段的延遲推向物理極限，提供極致流暢的 Agentic AI 互動體驗。
