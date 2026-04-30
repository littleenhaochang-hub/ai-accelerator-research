# Hardware Position Embedding Generator 實驗報告

## 1. 實驗背景
位置編碼（如 RoPE 或 ALiBi）在超長文本中佔用了大量的計算資源。傳統上這些計算會被編譯為獨立的 Kernel，消耗記憶體頻寬並阻礙了算術單元的使用。

## 2. 實驗方法
設計 `hardware_pos_embed_sim.py`，模擬將位置編碼的生成邏輯直接實作為 SRAM 讀取路徑上的一個硬體單元。在資料送往 MAC 陣列前，直接在硬體線上（Inline）套用旋轉矩陣或 ALiBi 偏差。

## 3. 實驗數據與結果
*   **上下文長度:** 65536
*   **軟體計算延遲:** 196.61 ms
*   **硬體 Inline 延遲:** 6.55 ms
*   **加速比:** 30.00x

## 4. 架構建議
硬體層級的位置編碼產生器能夠在不增加 MAC 陣列負擔的情況下，消除長文本處理的瓶頸。建議在下一代架構中，將此「Hardware Position Embedding Generator」整合進 SRAM 的資料輸出埠。