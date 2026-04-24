import time

def cpu_dom_parse(html_size_kb):
    # Simulated CPU software parsing (regex/BS4) latency (ms)
    return html_size_kb * 0.5 

def hw_fsm_dom_parse(html_size_kb):
    # Simulated Hardware Finite State Machine (FSM) parsing latency (ms)
    # Processing bytes stream directly at memory bandwidth speed
    return html_size_kb * 0.015

def main():
    html_size_kb = 2048 # 2MB typical raw DOM snapshot
    
    print("Running DOM Parsing Simulation for Edge Agentic AI...")
    cpu_lat = cpu_dom_parse(html_size_kb)
    print(f"CPU Software DOM Parsing Latency: {cpu_lat:.2f} ms")
    
    hw_lat = hw_fsm_dom_parse(html_size_kb)
    print(f"Hardware FSM DOM Minifier Latency: {hw_lat:.2f} ms")
    
    speedup = cpu_lat / hw_lat
    print(f"\nSpeedup: {speedup:.2f}x")

if __name__ == '__main__':
    main()
