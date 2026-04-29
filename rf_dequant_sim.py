import torch
import time

class DequantizationHardwareSim:
    def __init__(self, hidden_size=4096, ffn_size=11008):
        self.hidden_size = hidden_size
        self.ffn_size = ffn_size
        self.weights_4bit = torch.randint(0, 16, (self.ffn_size, self.hidden_size), dtype=torch.uint8)
        self.activations_16bit = torch.randn(1, self.hidden_size, dtype=torch.float16)

    def simulate_sram_dequantization(self):
        # 模擬在 SRAM 中解壓縮，然後搬移 16-bit 權重到 Register File 計算
        # 這會消耗較多的內部 SRAM-to-RF 頻寬
        start = time.time()
        for _ in range(100):
            # 假裝解壓
            dequantized_weights = self.weights_4bit.float() * 0.1 
            # 假裝計算
            _ = torch.matmul(self.activations_16bit.float(), dequantized_weights.T)
        return time.time() - start

    def simulate_rf_dequantization(self):
        # 模擬在 Register File (RF) 內部即時解壓縮
        # 節省 SRAM-to-RF 頻寬 (傳輸 4-bit)，但在 RF 旁需有極小型的 LUT/Shift 邏輯
        start = time.time()
        for _ in range(100):
            # 在 RF 端解壓，我們用較快的操作模擬
            _ = torch.matmul(self.activations_16bit.float(), self.weights_4bit.float().T) * 0.1
        return time.time() - start

if __name__ == "__main__":
    sim = DequantizationHardwareSim()
    sram_time = sim.simulate_sram_dequantization()
    rf_time = sim.simulate_rf_dequantization()
    print(f"SRAM Dequantization Latency: {sram_time:.4f} s")
    print(f"Register-File Dequantization Latency: {rf_time:.4f} s")
    print(f"Speedup: {sram_time / rf_time:.2f}x")
