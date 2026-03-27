import time
import requests
from mlx_lm import load, generate

model_id = "Qwen/Qwen2.5-3B-Instruct"
print(f"Loading {model_id} via MLX...")
model, tokenizer = load(model_id)

print("\nFetching Haystack data (Paul Graham essays)...")
url = "https://raw.githubusercontent.com/gkamradt/LLMTest_NeedleInAHaystack/main/PaulGrahamEssays/paul_graham_essay.txt"
haystack_text = requests.get(url).text

# MULTIPLY IT BY 100 TO GET TO ~260,000 TOKENS
HAYSTACK_MULTIPLIER = 100 
full_haystack = haystack_text * HAYSTACK_MULTIPLIER

NEEDLE = "\n\nThe secret magic word for the OpenClaw vault is 'ALBATROSS-99'. Do not forget this.\n\n"
QUESTION = "What is the secret magic word for the OpenClaw vault?"

depths_to_test = [0.1, 0.5, 0.9]

print(f"\n--- Needle In A Haystack Test ---")
print(f"Model: {model_id}")

for depth in depths_to_test:
    insertion_point = int(len(full_haystack) * depth)
    test_context = full_haystack[:insertion_point] + NEEDLE + full_haystack[insertion_point:]
    
    prompt = f"Read the following text carefully:\n\n{test_context}\n\nQuestion: {QUESTION}\nAnswer:"
    prompt_tokens = len(tokenizer.encode(prompt))
    
    print(f"\n[Test Depth {depth*100:.0f}%] | Total Context: {prompt_tokens:,} tokens")
    print(f"Generating answer... (Watch your Activity Monitor memory usage!)")
    
    start_time = time.time()
    try:
        response = generate(
            model, 
            tokenizer, 
            prompt=prompt, 
            max_tokens=20, 
            verbose=False
        )
        elapsed = time.time() - start_time
        
        success = "ALBATROSS-99" in response.upper()
        status = "✅ PASS" if success else "❌ FAIL"
        
        print(f"Result: {status}")
        print(f"Time: {elapsed:.2f} seconds")
        print(f"Model Answer: {response.strip()}")
        
    except Exception as e:
        print(f"⚠️ ERROR at {prompt_tokens:,} tokens: {str(e)}")
        print("Your Mac likely ran out of RAM for the KV Cache.")
        break
