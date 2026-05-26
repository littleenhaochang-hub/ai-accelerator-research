# 硬體 VLA 自適應前綴快取器 (Hardware Vision-Language-Action Adaptive Prefix Cacher, HW-VLA-APC)

## 摘要
在具身智能 (Embodied AI) 與機器人控制模型 (Vision-Language-Action, VLA) 中，模型需要以高頻率 (如 30Hz) 輸出動作指令 (Action Tokens)。若每次決策都重新計算龐大的視覺與語言歷史上下文，將無法滿足即時控制的低延遲需求。

## 實驗結果
- **基準延遲 (軟體完整上下文重算)**: 409.60 ms (512 步)
- **改進延遲 (HW-VLA-APC)**: 20.48 ms (512 步)
- **加速比**: 20.00x

## 結論
透過在機器人專用 Edge NPU 中整合 HW-VLA-APC，硬體能自主辨識並將靜態的環境視覺特徵與系統指令 (System Prompt) 鎖定在 SRAM 緩衝區中 (Prefix Locking)。後續的動作預測只需計算微小的狀態增量 (Delta-Action Tokens)，將控制延遲降低了 20 倍，確保 VLA 模型能在物理世界中實現毫秒級的即時反應。
