# Auto-Researcher 分析報告：Hardware Hybrid MoE-Dense Router (HMDR)

## 實驗背景
在混合專家 (MoE) 模型中，許多常見的語法或標點 Token 並不需要特定專家的深層知識，但傳統架構仍強制將其路由至特定專家，造成無謂的 PCIe 權重搬移與負載不均。

## 解決方案 (HMDR)
我們提出並模擬了 **硬體混合 MoE-Dense 路由器 (HMDR)** 架構。
在 NPU 中實作一個輕量級 Token 頻率分析器。當辨識出高度通用 (Common) 的 Token 時，直接繞過 MoE Routing，將其送入一個常駐在 SRAM 的共享小型 Dense FFN (Shared Expert) 中進行運算。

## 模擬數據 (hw_hybrid_moe_dense_router_sim.py)
* **Baseline Latency (Strict MoE)**: 52.00 ms
* **HMDR Latency (Shared FFN Routing)**: 14.50 ms
* **Throughput Speedup**: 3.59x

## 架構建議
建議將「HMDR 混合路由器」與 SRAM 常駐的「Shared Dense Expert」整合至 Edge NPU，以硬體手段過濾不必要的專家調用，極大化記憶體頻寬利用率。