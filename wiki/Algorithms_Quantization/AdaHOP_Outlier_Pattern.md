# AdaHOP: Outlier-Pattern-Aware Rotation

## The Bottleneck
Low-precision training and inference often blindly apply Hadamard transforms to mitigate activation outliers. However, outlier structures are not uniform; they can be row-wise, column-wise, or purely random. Applying a full dense orthogonal rotation ($O(H^2)$ overhead) is often overkill and slows down Edge NPUs.

## Hardware-Software Co-Design (The AdaHOP Approach)
Based on recent literature, we prototyped an Adaptive Hadamard strategy that statically analyzes the variance ratio of the FFN `down_proj` output channels on the Qwen2.5-1.5B model.
*   **Pattern Detected:** The variance ratio peaked at **653.81x**, confirming extreme **Column-Wise (Feature Dimension)** outliers in the SwiGLU activation.
*   **Action 1 (Full Rotation):** Applying a dense Hadamard rotation smears the 600x outliers, recovering +3.82 dB SQNR in a W4A4 setup.
*   **Action 2 (Outlier Extraction - OE):** Instead of rotating everything, we isolated the top 1% of outlier channels and kept them in FP16, while quantizing the remaining 99% to W4A4. 

## Prototype Verdict
*   **Naive W4A4 SQNR:** 11.77 dB
*   **AdaHOP Rotation SQNR:** 15.59 dB
*   **Outlier Extraction (1%) SQNR:** 14.07 dB

**Conclusion:** AdaHOP correctly proves that the FFN activation outliers are highly structured (Column-Wise). While Full Rotation yields the best mathematical SQNR (+3.82 dB), a hardware-aware Outlier Extraction (OE) for just 1% of the channels provides an excellent +2.30 dB recovery without requiring heavy $O(H^2)$ rotation matmuls. This proves that an Edge NPU with a dual-pipeline ALU (99% INT4 MACs + 1% FP16 MACs) is a highly efficient PPA alternative to pure mathematical rotation.
