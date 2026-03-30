# LLM Quantization Roadmap: Attention, FFN, and the Path to Sub-4-Bit
**Date:** March 31, 2026

## 1. 當前 Attention 與 FFN 的量化技術與極限 (Current State)

### Attention 層 (Q, K, V Projections & KV Cache)
*   **Activation (目前極限：4-bit + 1-bit 殘差 = 實質 5-bit)**
    *   **技術**：**TurboQuant (正交旋轉) + 1-Bit QJL 殘差**。Attention 的 Activation 存在極端離群值，單純 A4 會直接摧毀矩陣乘法。必須使用旋轉矩陣 (如 Hadamard/Householder) 將離群值抹平為高斯分佈，再配合 1-bit 殘差來拯救「Softmax 懸崖」(指數級誤差放大)。
*   **Weight (目前極限：4-bit)**
    *   **技術**：**Sub-channel 分組量化 (Group Size = 32/64)**。權重分佈穩定，不需旋轉。透過細粒度分組隔離誤差，搭配 FP16 Scale 即可維持極高精度。

### FFN 層 (MLP / Linear)
*   **Activation (目前極限：4-bit)**
    *   **技術**：**TurboQuant (正交旋轉)**。經過 SiLU/GeLU 激活函數後，FFN 的離群值比 Attention 更誇張。將旋轉矩陣整合進 FFN，可以完美抹平 Activation，且反向旋轉矩陣 $R^T$ 可提前「離線吸收」到下一層 Weight 中，達成推論時的 **零額外算力開銷 (Zero-Overhead)**。
*   **Weight (目前極限：4-bit)**
    *   **技術**：**Sub-channel 分組量化**。與 Attention 權重相同，靜態且呈常態分佈，切分 Block 即可完美壓至 W4。

---

## 2. 當前品質評估方法 (Quality Evaluation Methodology)
我們已經捨棄了單一的數學指標，全面採用 **「雙向驗證管線 (Dual-Validation Pipeline)」**：

1.  **Gate A: 數學 SNR (Signal-to-Noise Ratio)**
    *   測量硬體 MAC 層級的絕對誤差。區分 **Pre-Softmax SNR** (矩陣乘法精度) 與 **Post-Softmax SNR** (檢測 Softmax 懸崖的指數崩塌)。
2.  **Gate B: 模型實測 (Live LLM Generation)**
    *   Monkey-patch 攔截真實模型 (Qwen2.5-0.5B-Instruct) 的底層張量。
    *   執行 10-Prompt 綜合測試集 (涵蓋數學、程式、翻譯、常識)，檢驗模型在自迴歸 (Auto-regressive) 生成迴圈中是否會發生語意崩潰、幻覺或無限重複。

---

## 3. 下一步：如何突破更低位元 (Path to Sub-4-Bit: W3A3 / W2A4)

要將 Activation 和 Weight 進一步壓低到 3-bit 甚至 2-bit，傳統的 PTQ (Post-Training Quantization) 線性映射已經碰壁。下一步技術路徑如下：

### A. 針對 Weight (邁向 W3 / W2 / 1.58-bit)
1.  **Scale 的極限壓縮 (E8M0 / MX Formats)**：
    採納 OCP 的 Microscaling 標準。將 Sub-channel 的 FP16 Scale 強制壓縮為 **E8M0 (純指數無尾數)**。這不僅將 Scale 的記憶體頻寬砍半，更讓硬體乘法器 (Multiplier) 降級為極低功耗的整數加法器 (Bit-shift Adder)。
2.  **誤差補償與量化感知 (AWQ / GPTQ / QAT)**：
    到了 3-bit 以下，單純的分組切斷已經不夠。必須引入 Hessian 矩陣來評估權重的重要性 (GPTQ)，或是將量化誤差反向傳播回模型 (QAT)。單靠 PTQ 切換到 1.58-bit (BitNet) 會導致 SNR 暴跌至 5.8dB，必須依賴演算法層面的事前補償。

### B. 針對 Activation (邁向 A3)
1.  **非線性量化 (Non-linear LUT Quantization)**：
    放棄均勻等距的 Grid，改用查找表 (LUT) 根據高斯分佈的 CDF (累積分配函數) 來密集分配中段數值，稀疏分配極端數值 (如 NF4 的思維應用於 Activation)。
2.  **多位元殘差 (Multi-bit QJL)**：
    將 1-Bit 殘差升級。如果基準壓到 3-bit，搭配 1-bit 或 1.5-bit 的殘差，在硬體上依然可以使用極快的 Popcount 實現，但能用組合數學逼近 4-bit 甚至 5-bit 的動態範圍。

---

## 4. Auto-Researcher 下一步行動指南 (Next Steps)

Auto-Researcher 明日凌晨 (1:00 AM) 的自動執行任務將鎖定以下三大目標：

1.  **實作 E8M0 Scale 模擬器 (Pillar 2)**：
    將 Sub-channel 的 FP16 Scale 替換為 E8M0 純指數格式。驗證強制位移 (Bit-shift) 帶來的 dB 損失，確認是否值得換取「免乘法器 (Multiplier-Free)」的硬體紅利。
2.  **A3W3 + E8M0 的極限壓力測試 (Pillar 2 & 4)**：
    在 TurboQuant 的保護下，強行把 Activation 和 Weight 壓到 3-bit，並觀測 Qwen 0.5B 的生成成功率是否會從 40% 歸零。
3.  **推進 Pillar 7 (Test-Time Compute 路由架構)**：
    深化 DeepSeek-R1 / o1 的動態分支路由設計，解決 SIMT Warp Divergence 問題，這是當下最高優先級的硬體架構挑戰。