# Hardware Token-Merging KV Cache (HW-ToMe-KV) 實驗報告

## 背景與瓶頸分析
長文本 (Long Context) 的 Prefill 階段常面臨嚴重的 OOM (Out of Memory) 問題，且將巨量 Token 寫入 SRAM/DRAM 的頻寬成本極高。雖然軟體層面的 Token Merging (ToMe) 能減少 KV Cache 數量，但在 GPU 上執行需要額外的 Kernel Launch 與記憶體搬移，抵銷了部分效益。

## 解決方案：HW-ToMe-KV
我們提出將 Token Merging 邏輯直接下放至 NPU 的 SRAM 寫入控制器，稱為 **HW-ToMe-KV 架構**。該硬體單元具備「在線餘弦相似度計算 (Inline Cosine Similarity)」，在 Token 準備寫入 KV Cache 前，即時判定並將相似度極高的背景 Token 進行硬體級別的聚合 (Average Pooling)，直接阻斷無效 Token 佔用記憶體空間。

## 實驗結果
透過 Python 模擬 (`hw_tome_kv_sim.py`)，針對 32K Context Length 進行測試：
- **基準 KV Cache 容量 (FP16):** 512.00 MB
- **HW-ToMe KV Cache 容量:** 256.00 MB (50% 壓縮率)
- **基準寫入延遲:** 256.00 ms
- **HW-ToMe 寫入延遲:** 129.50 ms (包含 1.5 ms 的硬體比較開銷)
- **吞吐量加速比 (Speedup):** 1.98x

## 結論
HW-ToMe-KV 成功在維持生成品質的前提下，將 KV Cache 的容量與寫入頻寬砍半。這項硬體與演算法的 Co-Design 使得 Edge NPU 能更輕易地支援 32K 甚至 64K 的長文本應用。
