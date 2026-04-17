def simulate_lora_on_device(dim=4096, rank=16):
    print("Simulating On-Device LoRA PEFT Hardware Update Efficiency...")
    
    # 假設權重大小 W0 (FP16): 4096 * 4096 * 2 bytes = 32 MB
    w0_size_mb = (dim * dim * 2) / (1024 * 1024)
    
    # LoRA 權重 A 和 B 大小: (4096*16 + 16*4096) * 2 bytes = 256 KB
    lora_size_kb = (2 * dim * rank * 2) / 1024
    
    # DRAM 讀寫能耗 (每 GB 存取約消耗 10 mJ -> 每 MB 10 uJ)
    # SRAM 讀寫能耗 (每 MB 約消耗 0.1 uJ)
    dram_energy_per_mb = 10.0
    sram_energy_per_mb = 0.1
    
    # 傳統方法 (CPU/GPU-based):
    # 1. 從 DRAM 讀取 W0 (32 MB)
    # 2. 從 DRAM 讀取 A, B (0.25 MB)
    # 3. 計算 \Delta W = A * B
    # 4. W_new = W0 + \Delta W
    # 5. 寫回 W_new 到 DRAM (32 MB)
    traditional_dram_access_mb = w0_size_mb * 2 + (lora_size_kb / 1024)
    traditional_energy_uj = traditional_dram_access_mb * dram_energy_per_mb
    
    # In-SRAM Gradient Aggregation (NPU 直接更新):
    # 1. NPU 內部 SRAM 直接暫存 \Delta W
    # 2. 背景 DMA 讀取 W0 串流進入 NPU
    # 3. 在 NPU 內的 Weight Buffer 進行 W0 + \Delta W
    # 4. 直接寫回 DRAM (避免 CPU cache pollution)
    # 這免除了 A/B 矩陣的 DRAM 往返，並使用 SRAM 執行 \Delta W 累加
    # 能耗主要在 W0 的單次 Streaming I/O
    optimized_dram_access_mb = w0_size_mb * 2
    optimized_sram_access_mb = (lora_size_kb / 1024) * 3 # Read A, B, Write \Delta W
    optimized_energy_uj = (optimized_dram_access_mb * dram_energy_per_mb) + (optimized_sram_access_mb * sram_energy_per_mb)
    
    # 此外，如果 W0 被釘選在 Unified Memory 或 NPU SRAM (對於小模型)
    # In-SRAM 就可以完全免除 W0 的 DRAM 寫回！
    in_sram_update_energy_uj = (w0_size_mb * sram_energy_per_mb * 2) + (optimized_sram_access_mb * sram_energy_per_mb)
    
    print(f"Base Weight Size: {w0_size_mb} MB")
    print(f"LoRA Rank-{rank} Size: {lora_size_kb} KB")
    print(f"Traditional DRAM Update Energy: {traditional_energy_uj:.2f} uJ")
    print(f"Optimized DMA Update Energy: {optimized_energy_uj:.2f} uJ")
    print(f"Pure In-SRAM Update Energy: {in_sram_update_energy_uj:.2f} uJ")
    
    speedup = traditional_energy_uj / in_sram_update_energy_uj
    print(f"Hardware Energy Efficiency Gain (In-SRAM): {speedup:.2f}x")
    
    report_content = f"""# On-Device PEFT (LoRA) Hardware Simulation Report
## 背景 (Background)
Edge AI 逐漸走向在地化學習 (On-Device Learning)。微調 LLM 最常用的 LoRA (Low-Rank Adaptation) 在合併權重 ($W = W_0 + \Delta W$) 時，傳統架構會產生巨量的 CPU-DRAM 往返傳輸。

## 模擬參數 (Parameters)
- Hidden Dimension: {dim}
- LoRA Rank: {rank}
- W0 Size: {w0_size_mb} MB
- LoRA Weights Size: {lora_size_kb} KB

## 模擬結果 (Results)
- 傳統 CPU-DRAM 權重更新能耗: {traditional_energy_uj:.2f} µJ
- Pure In-SRAM (NPU 內部更新) 能耗: {in_sram_update_energy_uj:.2f} µJ
- 能源效率提升: {speedup:.2f}x

## 架構建議 (Architectural Proposal)
新一代 Edge NPU 必須包含 **In-SRAM Gradient Aggregator (SRAM 內梯度聚合器)**。這允許在 NPU 內部直接計算 $\Delta W = A \times B$ 並直接與 SRAM 中的 $W_0$ 進行 In-Place Addition，完全繞過耗電的 CPU 與 DRAM 匯流排。這對於依賴電池的行動裝置執行 Federated Learning 或 Personalization 微調至關重要。
"""
    with open("reports/lora_peft_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/lora_peft_report.md")

if __name__ == "__main__":
    simulate_lora_on_device()
