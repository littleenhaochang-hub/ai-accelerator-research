def simulate_bitnet_hardware(seq_len=1024, hidden_dim=4096):
    print("Simulating BitNet (1.58-bit) Ternary Hardware Efficiency vs INT8 MACs...")
    
    # 參數設定
    # 假設 FP16 MAC 消耗 1.5 pJ, INT8 MAC 消耗 0.2 pJ, INT32 Add 消耗 0.05 pJ
    energy_int8_mac_pj = 0.2
    energy_int_add_pj = 0.05
    
    # 矩陣相乘的運算次數 (以一個 Token 通過一個 QKV projection 為例)
    # MACs = hidden_dim * hidden_dim
    total_ops = hidden_dim * hidden_dim
    
    # 傳統 INT8 延遲與能耗
    int8_energy_nj = (total_ops * energy_int8_mac_pj) / 1000
    
    # BitNet (1.58-bit) 權重為 {-1, 0, 1}
    # 運算從 MAC (Multiply-Accumulate) 降級為純 Add/Sub (加減法)
    # 若權重為 0，則跳過運算 (假設 20% 的 0)
    sparsity = 0.20
    active_ops = total_ops * (1 - sparsity)
    bitnet_energy_nj = (active_ops * energy_int_add_pj) / 1000
    
    energy_reduction = int8_energy_nj / bitnet_energy_nj
    
    print(f"Hidden Dimension: {hidden_dim}")
    print(f"Total Operations per token: {total_ops}")
    print(f"INT8 MAC Energy: {int8_energy_nj:.2f} nJ")
    print(f"BitNet Add/Sub Energy (with 20% zeros): {bitnet_energy_nj:.2f} nJ")
    print(f"Energy Efficiency Gain: {energy_reduction:.2f}x")
    
    report_content = f"""# BitNet 1.58-bit (Ternary) Hardware Energy Report
## 背景 (Background)
BitNet b1.58 將 LLM 的權重量化為 {{-1, 0, 1}}，徹底淘汰了高能耗的浮點/整數乘法器，將矩陣乘法轉換為純加減法運算。

## 模擬參數 (Parameters)
- Hidden Dimension: {hidden_dim}
- INT8 MAC Energy: {energy_int8_mac_pj} pJ
- INT Add Energy: {energy_int_add_pj} pJ
- Ternary Sparsity (Zeros): {sparsity*100:.0f}%

## 模擬結果 (Results)
- 傳統 INT8 運算能耗: {int8_energy_nj:.2f} nJ
- BitNet 純加法運算能耗: {bitnet_energy_nj:.2f} nJ
- 硬體能效提升比 (Energy Efficiency Gain): {energy_reduction:.2f}x

## 架構建議 (Architectural Proposal)
未來的 Edge NPU 應配置專屬的 **Ternary ALU Arrays (三元加法器陣列)**，完全移除這些 Core 的 Multiplier 單元以節省矽面積 (Area)。配合權重中 0 的稀疏性 (Sparsity)，硬體應具備 Zero-Skipping 機制，達成 {energy_reduction:.2f} 倍以上的推論能效提升，這對於依靠電池供電的終端裝置至關重要。
"""
    with open("reports/bitnet_1_58_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/bitnet_1_58_report.md")

if __name__ == "__main__":
    simulate_bitnet_hardware()
