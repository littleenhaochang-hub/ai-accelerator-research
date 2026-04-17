# Mamba-2 State Space Duality (SSD) 硬體平行化分析

## 實驗背景
標準的 Mamba-1 (SSM) 雖然能解決 Transformer O(N^2) 的問題，但其依賴 O(N) 的序列掃描 (Sequential Scan)，難以充分利用現代 NPU/GPU 龐大的矩陣乘法單元 (Tensor Cores / MAC Arrays)。Mamba-2 提出了 State Space Duality (SSD) 理論，將 SSM 狀態更新轉換為分塊矩陣乘法 (Blocked Matrix Multiplication)。我們針對此架構進行了硬體運算延遲的模擬。

## 實驗方法
撰寫 `mamba2_ssd_sim.py`，模擬 16K Context 下 Mamba-1 循序掃描與 Mamba-2 SSD 分塊矩陣乘法 (Block Size = 256) 的執行延遲。

## 實驗數據
- **Context Length**: 16,384 tokens
- **Mamba-1 Sequential Scan Latency**: 819.20 ms
- **Mamba-2 SSD Blocked Latency**: 3.70 ms
- **Effective Speedup**: 221.41x

## 硬體架構結論
Mamba-2 SSD 架構透過將狀態空間模型轉化為矩陣運算，成功釋放了硬體高度平行化的能力，帶來了高達 **221.41 倍的加速**。
硬體設計上的關鍵啟發：與 Mamba-1 必須設計專用的硬體 Scan ALU Tree 相比，Mamba-2 的推論可以完美映射到現有的矩陣乘法器。未來的 Edge NPU 不需要為了 SSM 增加龐大的專用硬體模塊，只需在韌體層實作 **Tensor Core SSD Mapping (張量核心 SSD 映射)**，並優化 Block 間的狀態傳遞暫存器，即可無縫支援下一代線性複雜度模型。
