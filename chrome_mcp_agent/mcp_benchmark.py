import subprocess
import time
import json
import requests
import sys

# We'll use local Ollama for the benchmark since we are targeting edge agentic AI
OLLAMA_URL = "http://localhost:11434/api/generate"
# Fallback to llama3.2 (3B) which is fast for local inference
MODEL = "qwen2.5-coder:7b"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def mcp_open(url):
    print(f"  -> Opening: {url}")
    run_cmd(f'openclaw browser --browser-profile user open "{url}"')
    time.sleep(3) # Wait for page load

def mcp_snapshot():
    print("  -> Capturing DOM snapshot...")
    # Returns text formatted DOM
    return run_cmd('openclaw browser --browser-profile user snapshot --format text')

def run_llm_benchmark(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 128
        }
    }
    
    start_time = time.time()
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
    except Exception as e:
        print(f"  -> [Error] Local LLM failed: {e}")
        return None
        
    data = response.json()
    total_time = time.time() - start_time
    
    # Ollama returns these metrics in nanoseconds
    prompt_tokens = data.get("prompt_eval_count", 0)
    prompt_duration_ns = data.get("prompt_eval_duration", 1)
    
    output_tokens = data.get("eval_count", 0)
    output_duration_ns = data.get("eval_duration", 1)
    
    # Calculate TPS
    input_tps = prompt_tokens / (prompt_duration_ns / 1e9) if prompt_duration_ns > 0 else 0
    output_tps = output_tokens / (output_duration_ns / 1e9) if output_duration_ns > 0 else 0
    
    return {
        "response": data.get("response", ""),
        "input_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "input_tps": input_tps,
        "output_tps": output_tps,
        "total_latency": total_time
    }

use_cases = [
    {
        "name": "1. Research & Extraction (en.wikipedia.org)",
        "turns": [
            {
                "action": "open",
                "url": "https://en.wikipedia.org/wiki/Solid-state_drive",
                "prompt": "Extract the top 3 subheadings from this Wikipedia page DOM:"
            },
            {
                "action": "snapshot",
                "prompt": "Summarize the history section from this DOM:"
            }
        ]
    },
    {
        "name": "2. UI Navigation (news.ycombinator.com)",
        "turns": [
            {
                "action": "open",
                "url": "https://news.ycombinator.com",
                "prompt": "Find the DOM element ID or link for the top story:"
            },
            {
                "action": "snapshot",
                "prompt": "Identify the element ID for the 'Submit' button:"
            }
        ]
    },
    {
        "name": "3. Search & Form Fill (duckduckgo.com)",
        "turns": [
            {
                "action": "open",
                "url": "https://duckduckgo.com",
                "prompt": "Identify the input field ID to type a search query:"
            },
            {
                "action": "snapshot",
                "prompt": "Extract the CSS selector for the search button:"
            }
        ]
    }
]

print(f"Starting Chrome MCP Benchmark against Local Model: {MODEL}")
print("=" * 60)

for uc in use_cases:
    print(f"\n{uc['name']}")
    for i, turn in enumerate(uc['turns']):
        print(f" Turn {i+1}:")
        if turn["action"] == "open":
            mcp_open(turn["url"])
            
        dom = mcp_snapshot()
        # Truncate DOM to prevent local 8k context overflow
        dom_truncated = dom[:15000] 
        
        full_prompt = f"{turn['prompt']}\n\n{dom_truncated}"
        
        print("  -> Sending payload to LLM...")
        metrics = run_llm_benchmark(full_prompt)
        
        if metrics:
            print(f"  -> Result: {metrics['response'].split('.')[0]}...") # Truncate response
            print(f"  -> Metrics: In: {metrics['input_tokens']} tk ({metrics['input_tps']:.1f} TPS) | Out: {metrics['output_tokens']} tk ({metrics['output_tps']:.1f} TPS) | Latency: {metrics['total_latency']:.2f}s")
