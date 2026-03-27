import subprocess
import time
import os
import sys

try:
    from google import genai
except ImportError:
    print("google-genai not installed. Run: pip install google-genai")
    sys.exit(1)

if not os.environ.get("GEMINI_API_KEY"):
    print("[Error] GEMINI_API_KEY environment variable is not set.")
    sys.exit(1)

client = genai.Client()
MODEL = "gemini-2.5-flash"

def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def mcp_open(url):
    print(f"  -> Opening: {url}")
    run_cmd(f'openclaw browser --browser-profile user open "{url}"')
    time.sleep(3) # Wait for page load

def mcp_snapshot():
    print("  -> Capturing full DOM snapshot...")
    # Returns text formatted DOM
    return run_cmd('openclaw browser --browser-profile user snapshot --format text')

def run_llm_benchmark_streaming(prompt):
    start_time = time.time()
    try:
        response_stream = client.models.generate_content_stream(
            model=MODEL,
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
            
            # Extract usage from the final chunk if available
            usage = getattr(chunk, 'usage_metadata', None)
            if usage:
                prompt_tokens = usage.prompt_token_count
                output_tokens = usage.candidates_token_count
                
    except Exception as e:
        print(f"  -> [Error] Gemini API failed: {e}")
        return None
        
    end_time = time.time()
    
    # Metrics
    ttft = first_token_time - start_time
    generation_time = end_time - first_token_time
    total_latency = end_time - start_time
    
    # Calculate True TPS based on streamed timings
    input_tps = prompt_tokens / ttft if ttft > 0 else 0
    output_tps = output_tokens / generation_time if generation_time > 0 else 0
    
    return {
        "response": full_response,
        "input_tokens": prompt_tokens,
        "output_tokens": output_tokens,
        "ttft_s": ttft,
        "gen_time_s": generation_time,
        "input_tps": input_tps,
        "output_tps": output_tps,
        "total_latency": total_latency
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

print(f"Starting Streaming Chrome MCP Benchmark against Cloud Model: {MODEL}")
print("=" * 80)

for uc in use_cases:
    print(f"\n{uc['name']}")
    for i, turn in enumerate(uc['turns']):
        print(f" Turn {i+1}:")
        if turn["action"] == "open":
            mcp_open(turn["url"])
            
        dom = mcp_snapshot()
        full_prompt = f"{turn['prompt']}\n\n{dom}"
        
        print(f"  -> Sending payload to LLM ({len(dom):,} raw characters)...")
        metrics = run_llm_benchmark_streaming(full_prompt)
        
        if metrics:
            short_res = metrics['response'].replace('\n', ' ')[:60]
            print(f"  -> Result: {short_res}...")
            print(f"  -> Latency: TTFT {metrics['ttft_s']:.2f}s | Gen {metrics['gen_time_s']:.2f}s | Total {metrics['total_latency']:.2f}s")
            print(f"  -> True TPS: In: {metrics['input_tokens']:,} tk ({metrics['input_tps']:.1f} TPS) | Out: {metrics['output_tokens']:,} tk ({metrics['output_tps']:.1f} TPS)")
