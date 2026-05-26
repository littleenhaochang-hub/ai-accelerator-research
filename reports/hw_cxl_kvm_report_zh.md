# 硬體 CXL 解耦合 KV Cache 管理器 (HW-CXL-KVM) 模擬報告

## 1. 研究背景
隨著語言模型處理上下文長度 (Context Length) 的急遽增加 (如 128K 至 1M+ tokens)，Edge NPU 本機的 LPDDR/SRAM 容量已無法容納龐大的 KV Cache，導致頻繁的 Out-Of-Memory (OOM)。目前的妥協方案是將 KV Cache 換頁 (Swap) 至 NVMe SSD，但 PCIe Block I/O 的軟體驅動延遲使得推理性能暴跌。

## 2. 硬體架構創新 (HW-CXL-KVM)
為解決無限上下文帶來的記憶體容量瓶頸，我們提出 **硬體 CXL 解耦合 KV Cache 管理器 (Hardware CXL-Disaggregated KV Cache Manager, HW-CXL-KVM)**：
- **CXL 3.0 .mem 協定**：將傳統 NVMe PCIe 通道升級為 CXL (Compute Express Link) 3.0，使用記憶體語意 (Memory Semantics) 取代區塊設備語意 (Block I/O)。
- **硬體分頁與管理**：NPU 內建的 MMU 直接將 CXL 擴展記憶體映射為全域 KV Cache 池，完全繞過 CPU 中斷與 OS 虛擬記憶體管理。

## 3. 實驗與驗證
透過 `hw_cxl_kvm_sim.py` 模擬 KV Cache 分塊加載延遲：
- **Baseline (NVMe PCIe Block Swap)**: ~1664.55 ms
- **HW-CXL-KVM (CXL 3.0 Memory Semantic)**: ~312.70 ms
- **延遲加速比 (Speedup)**: **5.32x**

## 4. 結論與建議
實驗證實，改用 CXL 3.0 協定與硬體直接定址，可以將長文本 KV Cache 換頁延遲降低，獲得約 **5.32倍** 的性能提升。
**建議**：將 HW-CXL-KVM 引擎整合進新一代 Edge NPU 記憶體控制器中，以實現大容量且低延遲的解耦合記憶體架構 (Disaggregated Memory Architecture)。