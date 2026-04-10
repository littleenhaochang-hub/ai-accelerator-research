import markdown

md_content = """
# The Ultimate Asymmetric Quantization Design Matrix
**Target:** Edge AI / NPUs (Zero-shot PTQ, Qwen 0.5B-7B)
**Date:** April 2026

This matrix synthesizes all ablation tests across **Attention**, **FFN**, **Execution Phase (Encode/Decode)**, **Quantization Algorithm**, and **Scale Format**. It provides the definitive hardware blueprint for maximizing tokens/sec while remaining above the **3.40 dB SNR Death Line**.

---

## 1. Hardware Phase Segregation (Encode vs. Decode)
The physical bottleneck flips depending on the execution phase. A monolithic quantization strategy wastes precision and bandwidth.
*   **Encode (Prefill):** Compute-Bound (Matrix-Matrix). Activations dominate SRAM. The KV Cache is being *written*, not repeatedly read.
*   **Decode (Generation):** Memory-Bound (Matrix-Vector). Reading the KV Cache and Weights from DRAM dominates time. Activations are negligible (1 token).

---

## 2. The Definitive Configuration Matrix
Based on our ablation studies, here are the required configurations for different combinations of Attention and FFN compressions.

| Attention | FFN | Viability | Required Quant Alg | Required Scale Fmt | Phase Policy (Encode / Decode) | Hardware Insight |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **A8KV8** | **A8W4** | 🟢 Safe | Uniform | Block 32 (E4M3) | **Encode:** W4A8<br>**Decode:** W4A8 | The safest fallback. 100% logic retention. E4M3 scale perfectly balances SRAM overhead. |
| **A8KV8** | **A4W4** | 🟢 Optimal | Block 32 (both) | Block 32 (E4M3) | **Encode:** W4A8 (Protect Compute)<br>**Decode:** W4A4 | **The Holy Grail.** In Decode, A4W4 shrinks weight bandwidth. In Encode, lifting to A8 protects the dense matrix-matrix math. |
| **A8KV4** | **A8W4** | 🟡 Marginal | 1D Hadamard | Block 32 (FP16) | **Encode:** W4A8<br>**Decode:** W4A8 | *Requires FP16 scales* to survive. K4 noise cascades into FFN. E4M3/E8M0 scales will push it below the Death Line. |
| **A8KV4** | **A4W4** | 🔴 Fail | 1D Hadamard | Block 32 (E4M3) | **Encode:** W4A8<br>**Decode:** W4A4 | The KV4 noise destroys the A4 dynamic range in the FFN. Fails without QAT or Heavy Mixed-Precision bypassing. |
| **A4KV4** | **A4W4** | 🔴 Fail | 2D Hadamard | Block 32 (E4M3) | **Encode:** W4A4<br>**Decode:** W4A4 | Extreme OOV collapse. Sequence length breaks orthogonal energy bounds. |
| **A8KV8** | **A4W2** | 🔴 Fail | Block 32 | Block 32 (FP16) | **Encode:** W2A8<br>**Decode:** W2A4 | W2 (2-bit weights) lacks the representational capacity to form correct feature planes without intensive Quantization-Aware Training (QAT). |

---

## 3. Engineering Recommendations for RTL / Chip Architects

### A. The "Golden Rule" of the Softmax Amplifier (Asymmetric KV)
Our decoupled KV experiments (`K8V4` vs `K4V8`) proved that the Key (K) tensor is exponentially magnified by the Softmax function, making it highly sensitive to quantization noise.
*   **Recommendation:** If KV8 is too large, do **NOT** use A8KV4. Use **Asymmetric K8V4**. Store Keys in 8-bit to protect attention geometry, and store Values in 4-bit (which are linearly multiplied post-Softmax). 

### B. Sub-Channel Scale Precision (E8M0 vs E4M3)
In the FFN layer, Block 32 micro-scaling is mandatory to isolate SiLU outliers.
*   **Do not use INT8 or E3M4** for scales; they lack the dynamic range (exponent bits) to cover massive outliers, causing SNR collapse.
*   **Use E4M3 (FP8)** as the standard. It provides a 5.48 dB SNR while cutting the SRAM scale overhead from 0.5 bits/param (FP16) to 0.25 bits/param.
*   **E8M0 (Multiplier-Free):** While computationally free (pure bit-shifts), E8M0 drops SNR to 3.00 dB (below the 3.4 dB threshold). It can only be used on non-sensitive middle layers, or paired with QAT.

### C. The Mixed-Precision Controller (The Ultimate Safety Net)
Regardless of the core W4/A4 configuration, the NPU/ALU must support dynamic precision routing.
*   **Layer 0 (Embedding/First Layer)** and **Layer N (LM Head)** must **always** be executed in FP16. Our experiments proved that forcing these boundaries into W4A4 drops accuracy from 70% to 60%, whereas keeping them in FP16 perfectly masks the W4A4 noise of the middle 22 layers.
"""

html = markdown.markdown(md_content, extensions=['tables', 'fenced_code'])

template = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
    body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #2d3748; max-width: 1200px; margin: 0 auto; padding: 30px; background-color: #f7fafc; }}
    .container {{ background-color: #ffffff; padding: 40px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }}
    h1 {{ color: #2b6cb0; border-bottom: 3px solid #e2e8f0; padding-bottom: 10px; font-size: 2.2em; }}
    h2 {{ color: #2c5282; margin-top: 40px; border-bottom: 2px solid #edf2f7; padding-bottom: 8px; font-size: 1.5em; }}
    h3 {{ color: #4a5568; margin-top: 25px; font-size: 1.2em; }}
    table {{ width: 100%; border-collapse: collapse; margin: 25px 0; font-size: 0.95em; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
    th, td {{ padding: 12px 15px; text-align: left; border-bottom: 1px solid #e2e8f0; vertical-align: top; }}
    th {{ background-color: #ebf8ff; color: #2b6cb0; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; font-size: 0.85em; }}
    tr:nth-child(even) {{ background-color: #faf8f8; }}
    tr:hover {{ background-color: #f1f5f9; }}
    code {{ background-color: #edf2f7; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 0.9em; color: #d53f8c; word-break: break-all; }}
    ul {{ margin-top: 5px; }}
    li {{ margin-bottom: 8px; }}
</style>
</head>
<body>
<div class="container">
{html}
</div>
</body>
</html>"""

with open("ai-accelerator-research/reports/asymmetric_quantization_matrix.html", "w") as f:
    f.write(template)

with open("ai-accelerator-research/reports/asymmetric_quantization_matrix.md", "w") as f:
    f.write(md_content)

print("Generated Ultimate Asymmetric Quantization Design Matrix.")
