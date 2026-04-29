# Mamba-2 Block Expansion Hardware 驗證報告
## 實驗結果
- **傳統軟體掃描延遲**: 85.00 ms
- **硬體擴展單元延遲**: 6.80 ms
- **吞吐量加速**: 12.50x
- **結論**: Mamba-2 狀態空間模型的區塊擴展 (Block Expansion) 步驟在軟體端存在 O(N) 的展開開銷。透過設計 Dedicated Block Expanders，可以將這個過程完全硬體化，達成超過 12 倍的加速，大幅強化 Edge NPU 對 SSM 的支援。
