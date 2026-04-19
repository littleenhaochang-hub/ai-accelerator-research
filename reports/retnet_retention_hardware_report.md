# RetNet Retention 機制硬體架構分析報告

## 背景與瓶頸分析
傳統 Transformer 的 Attention 機制在處理極長文本時，KV Cache 的容量呈 O(N) 成長，造成邊緣裝置 (Edge NPU) 的 SRAM/DRAM 極大壓力。RetNet (Retentive Network) 提出了 Retention 機制，能將序列處理轉換為遞迴形式 (Recurrent Form)，將記憶體複雜度降為 O(1)。

## 解決方案：專用 Retention 狀態暫存器 (Hardware Retention State Cache)
為了充分發揮 RetNet 的優勢，我們提出在 NPU 中內建專用的「Retention 狀態暫存器區塊」。這允許模型在推論時將 O(1) 的狀態矩陣直接固定在 SRAM 中，無需像 KV Cache 那樣進行動態的記憶體分配和跨層的外部 DRAM 讀寫。

## 實驗結果
透過 Python 模擬 `retnet_retention_hardware_sim.py`：
- **傳統 Transformer KV Cache (32K Context):** 512.00 MB
- **RetNet 遞迴狀態記憶體 (O(1)):** 32.00 MB
- **記憶體縮減倍率 (Memory Reduction):** 16.00x

## 結論與架構建議
實驗證明，RetNet 在長文本推論上能大幅度削減記憶體使用量。
**硬體架構建議：** 建議未來的高效能 Edge NPU 將「KV Cache 管理單元」升級為支援矩陣乘法的「Retention 狀態維護引擎 (Retention State Engine)」，直接在暫存器層次處理 Retention 衰減運算 (Decay Operations)。
