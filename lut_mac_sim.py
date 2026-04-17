def simulate_lut_mac(dim=4096):
    print("Simulating LUT (Look-Up Table) vs MAC for Sub-4-bit Quantization...")
    
    # 假設 FP16 MAC 消耗 1.5 pJ
    # 假設 INT4 MAC 消耗 0.1 pJ
    # 假設 SRAM LUT 讀取消耗 0.02 pJ
    
    energy_fp16_mac = 1.5
    energy_int4_mac = 0.1
    energy_lut_read = 0.02
    
    total_ops = dim * dim
    
    fp16_energy = total_ops * energy_fp16_mac
    int4_energy = total_ops * energy_int4_mac
    
    # 對於 W4A4，我們可以預先計算 16x16 = 256 種可能的乘積，存入 LUT
    # 這樣每次運算只需要查表 (LUT Read) + 累加 (Accumulate 0.01 pJ)
    energy_accumulate = 0.01
    lut_energy = total_ops * (energy_lut_read + energy_accumulate)
    
    speedup_vs_int4 = int4_energy / lut_energy
    
    print(f"Dimension: {dim}")
    print(f"Total Operations: {total_ops}")
    print(f"INT4 MAC Energy: {int4_energy / 1e6:.2f} uJ")
    print(f"LUT-based Energy: {lut_energy / 1e6:.2f} uJ")
    print(f"Energy Efficiency Gain vs INT4 MAC: {speedup_vs_int4:.2f}x")
    
    report_content = f"""# LUT-based MAC for Sub-4-bit Quantization
## 背景 (Background)
在極低位元量化 (W4A4 或更低) 的情況下，運算元的值域非常小 (例如 4-bit 只有 16 種可能值)。與其使用傳統的乘法器 (Multiplier)，不如將所有可能的乘積預先計算好存入 Look-Up Table (LUT) 中。

## 模擬參數 (Parameters)
- Hidden Dimension: {dim}
- INT4 MAC 能量: {energy_int4_mac} pJ
- LUT 讀取能量: {energy_lut_read} pJ
- 累加器能量: {energy_accumulate} pJ

## 模擬結果 (Results)
- INT4 運算總能耗: {int4_energy / 1e6:.2f} µJ
- LUT 查表與累加總能耗: {lut_energy / 1e6:.2f} µJ
- 能效提升比: {speedup_vs_int4:.2f}x

## 架構建議 (Architectural Proposal)
為了極致降低 Edge NPU 的功耗，我們建議在 Tensor Core 內部整合分散式的 **Micro-SRAM LUTs**。當載入 W4A4 甚至 W2A2 的權重時，MAC Array 動態重構為 LUT 查表模式，完全關閉耗電的組合邏輯乘法器，僅保留加法樹，達成約 {speedup_vs_int4:.2f} 倍的推論能效提升。
"""
    with open("reports/lut_mac_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/lut_mac_report.md")

if __name__ == "__main__":
    simulate_lut_mac()
