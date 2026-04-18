# Edge NPU 記憶體架構分析：LPDDR5X vs HBM3

## 實驗背景
在設計 Edge AI Accelerator 時，記憶體介面的選擇決定了 PPA 的天花板。Cloud GPU 依賴高頻寬但高功耗的 HBM3，而 Edge NPU (如 Apple Silicon) 通常採用 Unified LPDDR5X。我們模擬了兩者在執行 70B W4A16 巨型模型時的吞吐量與能耗差異。

## 實驗方法
撰寫 `hbm_lpddr_sim.py`，模擬生成單一 Token 時讀取 35GB 權重的物理開銷。
- **HBM3**: 3000 GB/s, 3.5 pJ/bit
- **LPDDR5X**: 400 GB/s, 2.0 pJ/bit

## 實驗數據
- **HBM3 吞吐量**: 85.7 tok/s
- **HBM3 能耗**: 0.98 Joules / token
- **LPDDR5X 吞吐量**: 11.4 tok/s
- **LPDDR5X 能耗**: 0.56 Joules / token
- **LPDDR5X 節能比例**: 42.86%

## 硬體架構結論
LPDDR5X 展現了極佳的能效比，為 Edge 推論節省了約 42.86% 的 DRAM 讀取功耗。
然而，其帶寬僅為 HBM 的 1/7.5，導致 70B 模型的生成速度只有 11.4 tok/s，無法滿足即時互動的需求。為了在保有 LPDDR 節能優勢的同時彌補頻寬鴻溝，未來的 Edge NPU 不能依賴提升 DRAM 時脈，而是必須往兩個方向極致化：(1) 採用 Sub-3-bit (如 KIVI/AQLM) 極端權重量化，(2) 擴大 SRAM 容量並整合 Compute-In-Memory (CIM) 將運算下放，減少對 DRAM 的依賴。
