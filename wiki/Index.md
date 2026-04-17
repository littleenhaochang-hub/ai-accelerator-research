# 🧠 OpenClaw 硬件與演算法維基總覽 (Auto-Researcher Dashboard)

這是由自動研究員 (Auto-Researcher) 自動維護與更新的知識圖譜大廳。所有的研究節點、打樣程式碼與最新論文都會歸檔於下方列表中，點擊連結即可直接閱讀。

## 📊 知識庫狀態與導覽

### 📂 Algorithms Quantization
| 檔案連結 (File) | 知識主題 (Topic) | 自動收集的論文數 | 假說/原型數 |
| :--- | :--- | :---: | :---: |
| [`Compound_Noise_Analysis.md`](./Algorithms_Quantization/Compound_Noise_Analysis.md) | **Universal Benchmark (Compound Noise Analysis)** | - | - |
| [`Householder_TurboQuant.md`](./Algorithms_Quantization/Householder_TurboQuant.md) | **Householder TurboQuant** | - | - |
| [`NF4_LUT_Quantization.md`](./Algorithms_Quantization/NF4_LUT_Quantization.md) | **NF4 LUT Quantization vs Linear Bit-Shifting** | 📄 7 篇 | - |
| [`SpinQuant_FFN_Rotation.md`](./Algorithms_Quantization/SpinQuant_FFN_Rotation.md) | **SpinQuant: FFN Outlier Rotation & Smoothing** | - | - |

### 📂 Hardware Architecture
| 檔案連結 (File) | 知識主題 (Topic) | 自動收集的論文數 | 假說/原型數 |
| :--- | :--- | :---: | :---: |
| [`Adversarial_Hypotheses.md`](./Hardware_Architecture/Adversarial_Hypotheses.md) | **自主交叉探索與假說生成 (Adversarial Hypotheses)** | - | 🧠 3 個假說 |
| [`Autonomous_Prototypes.md`](./Hardware_Architecture/Autonomous_Prototypes.md) | **自主打樣與驗證日誌 (Autonomous Prototypes)** | - | 🧪 1 次打樣 |
| [`Cross_Family_Prefill.md`](./Hardware_Architecture/Cross_Family_Prefill.md) | **Cross-Family Speculative Prefill** | - | - |
| [`Emerging_Architectures.md`](./Hardware_Architecture/Emerging_Architectures.md) | **新興架構與未知探索 (Emerging Architectures)** | 📄 9 篇 | - |
| [`FP24_Accumulator.md`](./Hardware_Architecture/FP24_Accumulator.md) | **FP24 Accumulator** | - | - |
| [`MoE_Edge_Architecture.md`](./Hardware_Architecture/MoE_Edge_Architecture.md) | **MoE Edge Architecture (Gemma-4 26B)** | 📄 5 篇 | - |
| [`Model_Architecture_CoDesign.md`](./Hardware_Architecture/Model_Architecture_CoDesign.md) | **模型架構與演算法 (Model Architecture)** | 📄 4 篇 | - |
| [`Prefill_Sparse_Prediction.md`](./Hardware_Architecture/Prefill_Sparse_Prediction.md) | **Dynamic Sparse & Prefill Discoveries** | 📄 5 篇 | - |

- [MoE Speculative Prefetching](../reports/moe_prefetch_report.md) - PCIe bottleneck resolution via 90% accuracy lookahead predictors.
- [FlatQuant 4-bit Outliers](../reports/flatquant_report.md) - Resolving FFN activation outliers with hardware scaling units.
- [Long Context Prefill OOM](../reports/prefill_oom_report.md) - Householder 4-bit KV Cache and Chunked Attention to prevent 32K context memory overflow.
- [Mamba/SSM Hardware Parallel Scans](../reports/mamba_scan_report.md) - O(log N) hardware tree for SSM prefill acceleration.
- [W4A4 QJL Failure Analysis](../reports/qjl_quant_report.md) - Empirical rejection of QJL hardware due to SQNR collapse.
- [Speculative Decoding Tree Hardware](../reports/spec_decoding_report.md) - 15.4x TPS acceleration via hardware tree-mask generation for Draft verification.
- [Test-Time Compute Hardware](../reports/test_time_compute_report.md) - Energy-efficient System 2 reasoning via Hardware Weight Broadcasting for 16x parallel rollouts.
- [FlashAttention-3 Async TMA](../reports/fa3_report.md) - 1.99x speedup via fully asynchronous DMA ping-pong buffers.
- [Dynamic Token Pruning](../reports/token_pruning_report.md) - 31% power reduction via hardware SRAM token compaction.
- [DiT Adaptive Global-Local Attention](../reports/dit_attention_report.md) - 16x speedup for high-res Diffusion Transformers via SRAM-friendly local windows.
- [N:M Structured Sparsity](../reports/structured_sparsity_report.md) - 2x hardware throughput via 2:4 sparse tensor cores and metadata decoders.
- [Early-Exit Dynamic Depth](../reports/early_exit_report.md) - 30% energy savings via hardware confidence routers for shallow compute.
- [BitNet 1.58-bit Ternary Hardware](../reports/bitnet_158_report.md) - 62% power reduction by replacing MACs with addition-only ternary selectors.
- [DeepSeek MLA Hardware](../reports/mla_hardware_report.md) - 93.75% memory bandwidth reduction via on-the-fly latent vector up-projection.
- [SRAM Compute-in-Memory](../reports/cim_sram_report.md) - 91.3% energy reduction via analog bitline accumulation without weight movement.
