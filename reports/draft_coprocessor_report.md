# Speculative Decoding: Draft Co-Processor 硬體加速報告

## 背景分析
推測解碼 (Speculative Decoding) 是目前提升 LLM 推論速度最有效的方法之一。然而，在 Edge 裝置上，若讓 CPU 負責執行草稿模型 (Draft Model)，其生成延遲 (約 15ms/token) 過高，會大幅抵銷推測解碼帶來的好處，甚至與 NPU 產生記憶體頻寬競爭。

## 解決方案：專屬 Draft Co-Processor (草稿協同處理器)
我們提出在主 NPU 旁封裝一個超低功耗、小面積的「Draft Co-Processor」。該協處理器專門用於執行 100M~300M 參數級別的草稿模型 (如 EAGLE 或 Medusa heads)，並配備獨立的 SRAM 以避免與主 NPU 搶奪記憶體頻寬。草稿 Token 生成後，透過內部 FIFO 直接送入主 NPU 進行平行驗證。

## 實驗結果
透過 Python 模擬 `draft_coprocessor_sim.py`：
- **基礎 NPU 吞吐量 (無推測解碼):** 50.00 TPS
- **CPU 草稿生成推測解碼:** 61.54 TPS
- **Draft Co-Processor 推測解碼:** 153.85 TPS
- **加速比 (對比基礎):** 3.08x

## 結論與架構建議
專屬的草稿協處理器能將推測解碼的潛力完全釋放。建議未來的高階 Edge NPU 採用「一大一小 (Big.LITTLE)」的雙核心神經運算架構，小核專門負責 Draft 生成，大核負責 Target 驗證。
