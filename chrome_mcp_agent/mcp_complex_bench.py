import subprocess
import time
import os
import requests
import json
from google import genai

# Setup Gemini
if not os.environ.get("GEMINI_API_KEY"):
    print("[Error] GEMINI_API_KEY environment variable is not set.")
    exit(1)
client = genai.Client()
GEMINI_MODEL = "gemini-2.5-flash"

# Setup Ollama
OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "deepseek-coder-v2:16b"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def mcp_open(url):
    print(f"  -> Opening: {url}")
    run_cmd(f'openclaw browser --browser-profile user open "{url}"')
    time.sleep(4) # Wait for JS to render

def mcp_snapshot():
    print("  -> Capturing full DOM snapshot...")
    return run_cmd('openclaw browser --browser-profile user snapshot --format text')

def run_gemini(prompt):
    start_time = time.time()
    try:
        response_stream = client.models.generate_content_stream(
            model=GEMINI_MODEL,
            contents=prompt,
        )
        first_token_time = None
        full_response = ""
        prompt_tokens = 0
        output_tokens = 0
        for chunk in response_stream:
            if first_token_time is None:
                first_token_time = time.time()
            full_response += chunk.text
            usage = getattr(chunk, 'usage_metadata', None)
            if usage:
                prompt_tokens = usage.prompt_token_count
                output_tokens = usage.candidates_token_count
    except Exception as e:
        return {"error": str(e)}
        
    end_time = time.time()
    ttft = first_token_time - start_time if first_token_time else 0
    gen_time = end_time - first_token_time if first_token_time else 0
    
    in_tps = prompt_tokens / ttft if ttft > 0 else 0
    out_tps = output_tokens / gen_time if gen_time > 0 else 0
    
    return {
        "response": full_response,
        "in_tk": prompt_tokens, "out_tk": output_tokens,
        "in_tps": in_tps, "out_tps": out_tps,
        "latency": end_time - start_time
    }

def run_ollama(prompt):
    # Truncate to ~16k characters to prevent Ollama from instantly OOMing the Mac mini on 16B MoE
    # 16k chars is roughly 4k-5k tokens, fitting nicely in a local context limit
    truncated_prompt = prompt[:16000]
    
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": truncated_prompt,
        "stream": False,
        "options": {
            "num_predict": 128,
            "num_ctx": 8192
        }
    }
    start_time = time.time()
    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=300)
        res.raise_for_status()
    except Exception as e:
        return {"error": str(e)}
        
    data = res.json()
    prompt_tokens = data.get("prompt_eval_count", 0)
    prompt_duration_s = data.get("prompt_eval_duration", 1) / 1e9
    output_tokens = data.get("eval_count", 0)
    output_duration_s = data.get("eval_duration", 1) / 1e9
    
    return {
        "response": data.get("response", ""),
        "in_tk": prompt_tokens, "out_tk": output_tokens,
        "in_tps": prompt_tokens / prompt_duration_s if prompt_duration_s > 0 else 0,
        "out_tps": output_tokens / output_duration_s if output_duration_s > 0 else 0,
        "latency": time.time() - start_time
    }

# Complex 4-Turn Scenario: GitHub Analysis
turns = [
    {
        "action": "open",
        "url": "https://github.com/search?q=machine+learning&type=repositories",
        "prompt": "Identify the CSS selector or href link for the first repository in these search results."
    },
    {
        "action": "open",
        "url": "https://github.com/tensorflow/tensorflow",
        "prompt": "Extract the exact number of Stars and Forks from this repository page."
    },
    {
        "action": "snapshot",
        "prompt": "Find the link to the 'Issues' tab and output its exact href attribute."
    },
    {
        "action": "open",
        "url": "https://github.com/tensorflow/tensorflow/issues",
        "prompt": "Extract the title of the top open issue listed on this page."
    }
]

print("Starting Complex 4-Turn Chrome MCP Benchmark")
print(f"Models: Cloud ({GEMINI_MODEL}) vs Edge ({OLLAMA_MODEL})")
print("=" * 80)

for i, turn in enumerate(turns):
    print(f"\n[Turn {i+1}] {turn['prompt']}")
    if turn["action"] == "open":
        mcp_open(turn["url"])
    dom = mcp_snapshot()
    
    full_prompt = f"{turn['prompt']}\n\nDOM:\n{dom}"
    
    # 1. Gemini
    print(f"  -> Testing {GEMINI_MODEL} (Full DOM: {len(dom)} chars)...")
    gem_stats = run_gemini(full_prompt)
    if "error" not in gem_stats:
        res_short = gem_stats['response'].replace('\n', ' ')[:50]
        print(f"     Res: {res_short}...")
        print(f"     Stats: {gem_stats['latency']:.1f}s | In TPS: {gem_stats['in_tps']:.1f} ({gem_stats['in_tk']}tk) | Out TPS: {gem_stats['out_tps']:.1f} ({gem_stats['out_tk']}tk)")
    else:
        print(f"     Error: {gem_stats['error']}")
        
    # 2. DeepSeek (Ollama)
    print(f"  -> Testing {OLLAMA_MODEL} (Truncated DOM: 16k chars)...")
    ds_stats = run_ollama(full_prompt)
    if "error" not in ds_stats:
        res_short = ds_stats['response'].replace('\n', ' ')[:50]
        print(f"     Res: {res_short}...")
        print(f"     Stats: {ds_stats['latency']:.1f}s | In TPS: {ds_stats['in_tps']:.1f} ({ds_stats['in_tk']}tk) | Out TPS: {ds_stats['out_tps']:.1f} ({ds_stats['out_tk']}tk)")
    else:
        print(f"     Error: {ds_stats['error']}")
