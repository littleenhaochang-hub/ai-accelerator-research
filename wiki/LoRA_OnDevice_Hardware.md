# On-Device PEFT (LoRA) Hardware Architecture

## 實驗背景
為了達成 Edge 端個人化微調 (Personalization)，NPU 必須能高效執行 LoRA 更新。傳統的 $W = W_0 + \Delta W$ 操作會因為反覆存取 DRAM 導致巨大的耗電量。

## 硬體模擬與分析
- **腳本**: `lora_peft_sim.py`
- 對於一個 32MB 的權重層與 Rank-16 的 LoRA，傳統 DRAM 更新消耗約 642 µJ。
- 若 NPU 支援 **In-SRAM Update**，利用內部暫存器完成矩陣相乘與加法，能耗驟降至 6.48 µJ。
- **能效提升比**: 99.23x

## 架構協同設計結論
Edge NPU 的控制器必須實作 **In-SRAM Gradient Aggregator** 與硬體支援的 In-Place Addition。此架構能徹底避免 Base Model Weights 在 DRAM 與 CPU/NPU 之間的無謂搬運，為手機/筆電的終端 Federated Learning 鋪平道路。
