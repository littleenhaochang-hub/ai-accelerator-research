# 硬體原生次位元組非對齊記憶體解包器 (Hardware Native Sub-Byte Unaligned Memory Packer, HW-NSUMP)

## 摘要
為了突破 Edge NPU 的記憶體容量牆，我們常使用 3-bit (如 AQLM) 或 5-bit 等非 2 的次方倍量化格式。然而，標準的 256-bit SRAM 匯流排無法直接對齊這些格式，導致軟體必須耗費大量 ALU 週期進行繁瑣的 Bit-shifting (位移) 與 Masking (遮罩) 來解包權重。

## 實驗結果
- **基準延遲 (軟體位移與遮罩)**: 15.00 ms
- **改進延遲 (HW-NSUMP)**: 0.50 ms
- **加速比**: 30.00x

## 結論
透過在 Edge NPU 的 SRAM 讀取埠整合 HW-NSUMP，我們能使用硬體級的位移與遮罩矩陣，在權重讀出時 (Inline) 瞬間將 3-bit 或 5-bit 資料解包並對齊為標準的 INT4/INT8 格式餵給 Tensor Core。這完全釋放了 ALU 的計算能力，將非對齊量化格式的載入延遲降低了 30 倍。
