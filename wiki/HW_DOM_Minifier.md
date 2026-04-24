# Hardware DOM Minifier (硬體 DOM 壓縮引擎)

## 實驗背景 (Background)
根據我們在 Edge Agentic AI 的研究，當地端設備（如 Mac mini）執行自動化瀏覽器代理時，輸入的原始 DOM（通常大於 2MB，包含大量無用的 CSS/JS 標籤）會造成嚴重的長文本 Prefill OOM 與延遲。若使用 CPU (如 Python Regex / BeautifulSoup) 進行前處理，每回合會卡頓超過 1 秒鐘，嚴重拖累 Agent 的反應速度。

## 物理模擬 (Physical Simulation)
透過 `hw_dom_minifier_sim.py` 進行了 CPU 解析與硬體 FSM (Finite State Machine) 解析的效能對比：
- **CPU 軟體解析延遲 (2MB DOM)**: 1024.00 ms
- **硬體 FSM DOM 壓縮引擎延遲**: 30.72 ms
- **整體加速比**: 33.33x

## 架構提案 (Architectural Proposal)
我們提議在 NPU 的 Ingress Bus（輸入匯流排）前加裝 **「Hardware DOM Minifier Engine」**。
當 DMA 從主記憶體拉取網頁原始碼時，此引擎透過 In-line 的硬體狀態機 (FSM) 即時濾除 `<script>`, `<style>`, `<svg>` 等非語意標籤，並將 HTML 轉換為輕量化的 Accessibility Tree（Markdown 格式），直接寫入 NPU SRAM。這將徹底解決邊緣設備執行 Agentic AI 的前處理瓶頸，實現真正的 Real-time 本地網頁代理。
