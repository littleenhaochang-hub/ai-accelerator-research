def simulate_paged_attention_hardware(batch_size=32, max_seq_len=2048, page_size=16):
    print("Simulating PagedAttention Hardware Memory Fragmentation vs Contiguous Memory...")
    
    # 參數設定
    # 每個 token 佔用的 KV Cache 大小 (假設 2 bytes per param, 128 head dim, 32 heads)
    token_size_kb = (128 * 32 * 2 * 2) / 1024 
    
    # 傳統 Contiguous Memory (會因為預留最大長度而產生內部碎裂)
    # Total memory allocated = batch_size * max_seq_len * token_size
    contiguous_mem_mb = (batch_size * max_seq_len * token_size_kb) / 1024
    
    # 假設平均實際序列長度只有 512
    avg_seq_len = 512
    actual_used_mem_mb = (batch_size * avg_seq_len * token_size_kb) / 1024
    
    # PagedAttention Memory (動態分頁)
    # 只有需要的 page 才被 allocate
    pages_needed = (avg_seq_len + page_size - 1) // page_size
    paged_mem_mb = (batch_size * pages_needed * page_size * token_size_kb) / 1024
    
    waste_contiguous = contiguous_mem_mb - actual_used_mem_mb
    waste_paged = paged_mem_mb - actual_used_mem_mb
    
    memory_efficiency_gain = contiguous_mem_mb / paged_mem_mb
    
    print(f"Batch Size: {batch_size}, Max Seq: {max_seq_len}, Avg Seq: {avg_seq_len}")
    print(f"Contiguous Memory Allocated: {contiguous_mem_mb:.2f} MB")
    print(f"Paged Memory Allocated: {paged_mem_mb:.2f} MB")
    print(f"Waste (Contiguous): {waste_contiguous:.2f} MB")
    print(f"Waste (Paged): {waste_paged:.2f} MB")
    print(f"Memory Efficiency Gain: {memory_efficiency_gain:.2f}x")
    
    report_content = f"""# PagedAttention Hardware MMU Report
## 背景 (Background)
PagedAttention 解決了 LLM 推論中 KV Cache 嚴重的記憶體碎裂 (Memory Fragmentation) 問題。傳統推論框架必須為每個 Request 預先分配最大序列長度的連續記憶體。

## 模擬參數 (Parameters)
- Batch Size: {batch_size}
- Max Seq Length: {max_seq_len}
- Avg Seq Length: {avg_seq_len}
- Page Size: {page_size} tokens

## 模擬結果 (Results)
- 連續記憶體配置 (Contiguous): {contiguous_mem_mb:.2f} MB
- 分頁記憶體配置 (Paged): {paged_mem_mb:.2f} MB
- 記憶體使用效率提升: {memory_efficiency_gain:.2f}x

## 架構建議 (Architectural Proposal)
為了讓 Edge NPU 原生支援 PagedAttention，NPU 內部必須實作專屬的 **Hardware MMU (Memory Management Unit) for Tensors**。這允許 NPU 的 DMA 引擎直接使用 Page Table 來讀取分散的 KV Cache Blocks，無需依賴 CPU 介入進行虛擬位址到實體位址的轉換，徹底消除 OS 層級的 Context Switch 延遲。
"""
    with open("reports/paged_attention_report.md", "w", encoding="utf-8") as f:
        f.write(report_content)
    print("Simulation complete. Report written to reports/paged_attention_report.md")

if __name__ == "__main__":
    simulate_paged_attention_hardware()
