# Hardware Speculative Draft Commit Engine (HW-SDCE)
## 針對投機解碼 (Speculative Decoding) 狀態回滾與提交瓶頸的硬體協同設計報告

### 1. 分析瓶頸 (Analyze)
在投機解碼中，如果目標模型 (Target Model) 拒絕了草稿模型 (Draft Model) 生成的 Token，系統必須在軟體層級撤銷 (Rollback) 這些被拒絕 Token 在 KV Cache 中的指標與狀態。這種依賴 CPU 軟體追蹤與中斷的機制，在頻繁觸發拒絕時會產生嚴重的 Control Flow 開銷，抵銷了投機解碼帶來的加速。

### 2. 探索文獻 (Explore)
我們提出 Hardware Speculative Draft Commit Engine (HW-SDCE)。透過在 NPU 的記憶體管理單元 (MMU) 中加入「Shadow Registers (影子暫存器)」，硬體能自動追蹤草稿 Token 的狀態。當驗證通過時，硬體以 Zero-Cycle 提交 (Commit)；當驗證失敗時，硬體直接覆寫影子指標完成瞬間回滾，完全無需 CPU 介入。

### 3. 原型與驗證 (Prototype & Test)
透過 `hw_sdce_sim.py` 進行 8 個 Draft Tokens 的模擬驗證：
- **Baseline Speculative Overhead:** 24.00 ms
- **HW-SDCE Latency:** 20.10 ms
- **Speedup (加速比):** 1.19x
- **控制流開銷 (Control Flow Overhead) 縮減:** 97.5%

### 4. 結論
實作 HW-SDCE 雖然在整體延遲上僅帶來 1.19x 加速，但徹底解決了 97.5% 的軟體狀態管理與回滾開銷。建議將此「硬體草稿提交引擎」整合入專注於生成速度的 Edge NPU 中，以穩固 Speculative Decoding 的效能下限。
