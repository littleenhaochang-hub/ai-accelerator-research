# FlashAttention-3: Async TMA & Hardware Overlap

## 實驗背景
根據 FlashAttention-3 的核心精神 (Warp-Specialization 與 Async TMA)，我們模擬了在 Edge NPU 上的 SRAM 雙緩衝機制 (Ping-Pong Buffering)。目的在於將記憶體存取延遲完全隱藏在計算延遲之下。

## 硬體模擬與分析
- **腳本**: `flash_attn_sim.py`
- 模擬在 8K Context 下，Block TMA (0.049 µs) 與 Block Compute (0.209 µs) 的時間。
- 透過異步重疊 (Async Overlap)，總延遲從 16.57 µs 降至 13.47 µs。
- **加速比**: 1.23x (確保硬體維持 Compute-Bound)。

## 架構協同設計結論
Edge AI 晶片應導入「獨立的 Async DMA 引擎」與「雙/多緩衝 SRAM (Ping-Pong SRAM)」。這允許 MAC Array 進行 GEMM 運算的同時，背景可非同步載入下一個 Block 的 K/V 特徵，逼近 100% 的硬體利用率 (Utilization)。
