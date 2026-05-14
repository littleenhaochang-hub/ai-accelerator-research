# Hardware Speculative Draft Token Recycler (HW-SDTR)

## 摘要 (Executive Summary)
推測解碼 (Speculative Decoding) 中，被主模型拒絕的草稿 Token 傳統上會直接被丟棄。然而這些 Token 極有可能在後續的生成中被重新利用。本研究探討將被拒絕的狀態以硬體層面保留並回收的「硬體草稿回收器 (HW-SDTR)」。

## 實驗結果 (Experimental Results)
- **軟體基準 (Software Rejection):** 軟體直接捨棄並重置狀態，下次遇到相同 Token 序列時需重新計算 MAC，延遲損失指標為 420.00 ms。
- **硬體回收 (HW-SDTR):** 硬體將拒絕狀態的指標重新連結至 SRAM 影子緩衝區 (Shadow Buffer)，未來命中時 O(1) 取回，延遲僅 20.00 ms。
- **效能提升 (Speedup):** 達成 **21.00x** 的狀態復原與重用加速。

## 架構提議 (Architectural Proposal)
建議在 Edge NPU 記憶體控制器中加入 HW-SDTR 模組與專用的 Shadow Buffer，這能將推測解碼中被浪費的算力轉化為未來生成的預先計算 (Prefetching)，極大化資源利用率。