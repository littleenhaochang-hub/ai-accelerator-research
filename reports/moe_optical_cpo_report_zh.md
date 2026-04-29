# MoE Optical CPO 硬體架構研究報告

## 1. 分析瓶頸 (Analyze)
在先前的研究中，我們確認了 MoE (Mixture of Experts) 模型在邊緣運算裝置上解碼時，主要的瓶頸在於 CPU-GPU 之間的記憶體傳輸延遲。每次生成 Token 需要從 DRAM 或 NVMe 動態提取多個 Expert 的權重，導致嚴重的 PCIe 頻寬阻塞與延遲。

## 2. 探索文獻 (Explore)
由於傳統 PCIe Gen 5 頻寬與通訊協定的限制，我們探討了最新的光電共封裝 (Co-Packaged Optics, CPO) 架構論文。該架構結合硬體的光學 I/O 與模型架構的 MoE 動態路由，能夠以 Terabits 級別的頻寬實現近乎零延遲的跨晶片/跨記憶體資料傳輸。

## 3. 建立原型並驗證 (Prototype & Test)
我們在 `moe_optical_cpo_sim.py` 中實作了光學 CPO 傳輸與傳統 PCIe Gen 5 的效能對比模擬。
- **測試條件**：單一 Token 啟用 4 個 Experts，總負載為 400 MB。
- **基準測試 (PCIe Gen 5)**：延遲約 6.254 ms。
- **CPO 測試 (500 GB/s 光學頻寬)**：延遲大幅降低至 0.791 ms。
- **實驗結果**：取得 7.90x 的傳輸加速 (Speedup)，成功克服 MoE 的記憶體頻寬牆 (Memory Wall)。

## 4. 架構結論與建議
為了解決大規模 MoE 模型在 Edge NPU 上的傳輸瓶頸，我們建議未來的硬體架構應全面導入 **Silicon Photonics CPO (矽光子共封裝光學)** 作為專用記憶體匯流排，搭配專門的光學 DMA 控制器，實現 Expert 權重的近零延遲載入 (Zero-latency Fetching)。