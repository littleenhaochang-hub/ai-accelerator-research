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

def run_llm_benchmark(prompt):
    start_time = time.time()
    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
        )
    except Exception as e:
        print(f"  -> [Error] Gemini API failed: {e}")
        return None
        
    total_time = time.time() - start_time
    
    # Extract token usage from the response metadata
    usage = getattr(response, 'usage_metadata', None)
    prompt_tokens = usage.prompt_token_count if usage else 0
    output_tokens = usage.candidates_token_count if usage else 0
    
    # For cloud APIs, time-to-first-token is hard to separate without streaming,
    # so we calculate an "effective" TPS over the total network roundtrip.
    input_tps = prompt_tokens / total_time if total_time > 0 else 0
    output_tps = output_tokens / total_time if total_time > 0 else 0
    
    return {
        "response": response.text,
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

print(f"Starting Chrome MCP Benchmark against Cloud Model: {MODEL}")
print("=" * 60)

for uc in use_cases:
    print(f"\n{uc['name']}")
    for i, turn in enumerate(uc['turns']):
        print(f" Turn {i+1}:")
        if turn["action"] == "open":
            mcp_open(turn["url"])
            
        dom = mcp_snapshot()
        # Feed the FULL DOM (no truncation) to leverage Gemini's massive context window
        full_prompt = f"{turn['prompt']}\n\n{dom}"
        
        print(f"  -> Sending payload to LLM ({len(dom):,} raw characters)...")
        metrics = run_llm_benchmark(full_prompt)
        
        if metrics:
            short_res = metrics['response'].replace('\n', ' ')[:60]
            print(f"  -> Result: {short_res}...")
            print(f"  -> Metrics: In: {metrics['input_tokens']:,} tk | Out: {metrics['output_tokens']:,} tk | Latency: {metrics['total_latency']:.2f}s")
            # Calculate effective TPS (combining input processing and output generation over network)
            print(f"  -> Effective Network Throughput: {metrics['input_tps']:.1f} In-TPS | {metrics['output_tps']:.1f} Out-TPS")
