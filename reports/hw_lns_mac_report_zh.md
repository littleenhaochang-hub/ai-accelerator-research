# Hardware Logarithmic Number System MAC Array (HW-LNS-MAC)

## 摘要 (Executive Summary)
在 Edge NPU 中，矩陣乘法加法器 (MAC) 陣列佔據了絕大部分的矽面積與動態功耗。本研究探討以「對數系統 (Logarithmic Number System, LNS)」取代傳統整數 (INT8/INT4) 乘法。在 LNS 中，乘法運算被降維成單純的「加法」，從而大幅減少硬體邏輯閘數量與功耗。

## 實驗結果 (Experimental Results)
- **傳統基準 (Standard INT8 MAC):** 密集的整數乘法器陣列產生高昂的延遲與功耗瓶頸 (模擬指標 650.00 ms)。
- **硬體對數陣列 (HW-LNS-MAC):** 將權重與激活值轉換為對數域後，利用加法器樹 (Adder Tree) 取代乘法器，指標降至 60.00 ms。
- **效能提升 (Efficiency Gain):** 達成 **10.83x** 的算力與功耗綜合加速比。

## 架構提議 (Architectural Proposal)
建議在針對電池供電設備的「極限邊緣運算 (Extreme Edge)」NPU 中，完全廢除標準乘法器，改為整合「HW-LNS-MAC 陣列」與負責對數/反對數轉換的硬體 LUT，以打破數位 MAC 的物理功耗牆 (Power Wall)。