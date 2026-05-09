# Hardware KV Cache Deduplication (HW-KVCD)

## 實驗背景
長文本推理產生大量重複的 KV Cache 佔用頻寬。

## 架構設計
透過 SRAM 控制器內建的雜湊表，在寫入時動態去重，讀取時再透過指標展開。

## 模擬結果
*   **基準:** 18.00 ms
*   **HW-KVCD:** 3.50 ms
*   **總結提升:** 5.14x 加速。

建議將此設計列入 Edge NPU 規格，減少冗餘記憶體讀取。