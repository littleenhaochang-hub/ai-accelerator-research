import time
import requests
from mlx_lm import load, generate

model_id = "Qwen/Qwen3-4B-Instruct-2507"
print(f"Loading {model_id} via MLX...")
model, tokenizer = load(model_id)

print("\nFetching Haystack data (Pride & Prejudice from Project Gutenberg)...")
url = "https://www.gutenberg.org/cache/epub/1342/pg1342.txt"
haystack_text = requests.get(url).text

# Encode to tokens so we can slice EXACTLY 100,000 tokens
print("Tokenizing base text...")
tokens = tokenizer.encode(haystack_text)

# If the book isn't long enough, multiply it
if len(tokens) < 100000:
    haystack_text = haystack_text * (100000 // len(tokens) + 2)
    tokens = tokenizer.encode(haystack_text)

# Slice exactly 99,900 tokens (leaving room for the needle and prompt)
haystack_tokens = tokens[:99900]
full_haystack = tokenizer.decode(haystack_tokens)

NEEDLE = "\n\nThe secret magic word for the OpenClaw vault is 'ALBATROSS-99'. Do not forget this.\n\n"
QUESTION = "What is the secret magic word for the OpenClaw vault?"

depths_to_test = [0.1, 0.5, 0.9]

print(f"\n--- Needle In A Haystack Test (100K Tokens) ---")
print(f"Model: {model_id}")

for depth in depths_to_test:
    # Character index approximation for depth
    insertion_point = int(len(full_haystack) * depth)
    test_context = full_haystack[:insertion_point] + NEEDLE + full_haystack[insertion_point:]
    
    prompt = f"Read the following text carefully:\n\n{test_context}\n\nQuestion: {QUESTION}\nAnswer:"
    prompt_tokens = len(tokenizer.encode(prompt))
    
    print(f"\n[Test Depth {depth*100:.0f}%] | Total Context: {prompt_tokens:,} tokens")
    print(f"Generating answer... (This will take a minute to process the prompt)")
    
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
        break