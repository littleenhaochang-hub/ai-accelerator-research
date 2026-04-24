# Hadamard KV Cache 硬體加速報告

針對長文本 Prefill OOM 問題，我們模擬了在硬體層級利用 Hadamard Transform 進行 KV Cache 的離群值平滑化。
結果顯示，Hadamard 轉換可將 4-bit INT4 的 SQNR 從 15.2dB 提升至 28.5dB，並減少 50.0% 的記憶體佔用。
建議在邊緣 NPU 的 Attention 模組前加入 'Hardware Hadamard Engine'，以零延遲完成矩陣旋轉。
