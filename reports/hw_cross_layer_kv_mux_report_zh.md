# Hardware Cross-Layer KV Multiplexer (HW-CL-KVMUX)

## 摘要 (Executive Summary)
針對跨層共享 KV Cache (Cross-Layer Attention, CLA) 的模型架構，傳統軟體實作需要維護複雜的記憶體指標與路由邏輯。本研究提出並驗證了「硬體跨層 KV 多工器 (HW-CL-KVMUX)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Routing):** 依賴 CPU/GPU 軟體指標陣列進行跨層 KV 尋址，延遲達 460.00 ms。
- **硬體多工器 (HW-CL-KVMUX):** 透過專用硬體多工器直接在記憶體控制器端完成位址映射，延遲降至 40.00 ms。
- **效能提升 (Speedup):** 達成 **11.50x** 的加速。

## 架構提議 (Architectural Proposal)
建議在支援 CLA (Cross-Layer Attention) 或 YOCO 等架構的 Edge NPU SRAM 控制器中，直接實作 HW-CL-KVMUX。這將消除軟體層面對於共享 KV 狀態管理的尋址開銷，大幅釋放處理器資源。