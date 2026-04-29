# AI Accelerator Wiki

## Hardware Architectures
- [Dual-Pipe MoE Hardware Scheduler](../reports/dual_pipe_moe_report_zh.md): 雙管線 MoE 提取機制，針對 DeepSeek-V3 架構隱藏專家路由延遲。
- [Prefix Tuning Hardware Offloading](../reports/prefix_tuning_hardware_report.md): 透過硬體 MMU 將虛擬 Prefix 分頁直接映射至實體 KV 暫存，達到零拷貝 PEFT。
- [LoRA Context Switch Hardware](../reports/lora_switch_hardware_report.md): 透過 SRAM Bank 切換達成零週期 LoRA 權重置換。
- [In-SRAM LoRA Merging Hardware](../reports/insram_lora_merge_report.md): 在 SRAM 讀取放大器端整合微型加法器，實現讀取時動態零成本 LoRA 合併，針對多 Agent 環境極度最佳化。
- [Dynamic Precision KV Controller](../reports/dynamic_precision_kv_report.md): 根據注意力分數即時調降背景 Token 精確度至 INT2，保留 Sink Token 在 FP16，大幅減少記憶體頻寬需求。
- [Ternary KV Cache Hardware](../reports/ternary_kv_cache_report.md): 1.58-bit KV 狀態壓縮引擎，挑戰無窮上下文之記憶體物理極限。
- [SWA Ring Buffer Hardware](../reports/swa_ring_buffer_report.md): 在 SRAM 控制器實作硬體指標，以零延遲支援 Mistral 滑動窗口注意力的自動覆寫與模數尋址。- [Mamba State Decay Engine](../reports/mamba_decay_engine_report.md): 在 SRAM 控制器端內建專用衰減乘法器，加速 SSM 時間衰減矩陣更新，達 6.6 倍速。
- [DCT KV Cache Compression Hardware](../reports/dct_kv_cache_report.md): 在 SRAM 控制器內建硬體 DCT/IDCT 引擎，透過頻域轉換大幅壓縮長文本 KV Cache，達 6.2 倍速。

- [KAN B-Spline SRAM LUT Hardware](../reports/spline_lut_kan_report.md) - 2026-04-25
- [Hardware Dynamic Attention Head Gating (HDAG)](../reports/head_gating_hw_report.md) - 2026-04-25
- [Dynamic Hardware Precision Scaling (DHPS)](../reports/dhps_hw_report.md) - 2026-04-25
- [Analog PIM Crossbar Attention](../reports/analog_pim_attention_report.md) - 2026-04-25
- [Hyperdimensional Computing (HDC) XOR Attention Hardware](../reports/hdc_attention_hw_report.md) - 2026-04-25
- [Hardware Chunk-wise Parallel Linear Attention (CPLA)](../reports/cpla_hw_report.md) - 2026-04-25
- [SRAM Cuckoo Hash MoE Routing Hardware](../reports/cuckoo_moe_routing_report.md) - 2026-04-25
- [SRAM Bit-Serial Compute-in-Memory (CIM)](../reports/bit_serial_cim_report.md) - 2026-04-25
- [Hardware Bloom Filter MoE Routing](../reports/bloom_moe_routing_report.md) - 2026-04-26
- [Hardware-Accelerated Reversible Transformer Training](../reports/revnet_training_report.md) - 2026-04-26
- [Hardware Flash-FFT Attention](../reports/flash_fft_hw_report.md) - 2026-04-26
- [Hardware RWKV Time-Mixer Engine](../reports/rwkv_time_mixer_report.md) - 2026-04-26
- [Dual-Path Outlier Hardware (DPOH)](../reports/dual_path_outlier_hw_report.md) - 2026-04-26
- [Hardware Speculative Draft Verifier (HSDV)](../reports/hsdv_tree_verification_report.md) - 2026-04-26
- [Hardware Delta-Activation Engine (DAE)](../reports/delta_activation_hw_report.md) - 2026-04-26
- [[MoE P2P Ring DMA Hardware]] - Direct NVMe to NPU expert fetching bypassing CPU.
- [[Stochastic Computing Hardware]] - Sub-1-bit bitstream logic gate ALUs.
- [[Hardware Huffman MoE Decompressor]] - Inline variable-length decompression for weights.
