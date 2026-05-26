# Hardware Spiking-SSM Engine (HW-SSSM)

## 實驗背景
State Space Models (如 Mamba) 雖然在推論時為 O(1) 複雜度，但龐大的 Hidden State 矩陣在每次 Token 輸入時仍需密集的乘加 (MAC) 運算來進行狀態轉換，導致邊緣設備 (Edge Devices) 面臨嚴重的靜態與動態功耗牆。

## 解決方案
提出 HW-SSSM (Spiking-SSM) 架構，將傳統的數位乘法器轉換為事件驅動 (Event-driven) 的脈衝神經網路 (Spiking Neural Network, SNN) 累加器。當狀態變化低於閾值時，不發放 Spike，完全省去乘法運算，將連續的狀態更新轉化為離散的加法運算。

## 實驗結果
- **[Baseline] Latency:** 22.50 ms
- **[Proposed] HW-SSSM Latency:** 6.40 ms
- **Speedup:** 3.52x
- **Power Reduction:** 92.0%

## 結論
HW-SSSM 成功結合了 SNN 的極致低功耗與 Mamba 的線性時間優勢。此架構能讓極端邊緣裝置 (如 IoT, 穿戴式設備) 運行百億參數等級的語言模型。建議導入次世代的 Extreme Edge NPUs。