import torch
import torch.nn as nn
import time

class StandardEmbedding(nn.Module):
    def __init__(self, vocab_size, d_model):
        super().__init__()
        self.embed = nn.Embedding(vocab_size, d_model)
        
    def forward(self, input_ids):
        return self.embed(input_ids)

class HashEmbedding(nn.Module):
    def __init__(self, vocab_size, num_buckets, d_model):
        super().__init__()
        # Instead of storing 32k vectors, we store a small pool of vectors
        self.hash_table = nn.Embedding(num_buckets, d_model)
        # Optional: A tiny projection layer to mix the hashed vector
        self.proj = nn.Linear(d_model, d_model, bias=False)
        self.num_buckets = num_buckets
        
    def forward(self, input_ids):
        # Deterministic simple hash function modulo bucket size
        hashed_ids = input_ids % self.num_buckets
        hashed_embeds = self.hash_table(hashed_ids)
        return self.proj(hashed_embeds)

def simulate_hash_embeddings():
    torch.manual_seed(42)
    vocab_size = 32000
    d_model = 4096
    num_buckets = 4096  # 8x compression factor
    batch_size, seq_len = 1, 1024
    
    print(f"Initializing Tableless Hash Embeddings Baseline (Vocab: {vocab_size}, Dim: {d_model})")
    print(f"Standard Embedding Memory : {vocab_size * d_model * 2 / 1024 / 1024:.2f} MB (FP16)")
    print(f"Hash Embedding Memory     : {num_buckets * d_model * 2 / 1024 / 1024:.2f} MB (FP16) -> 8x Reduction")
    
    input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
    
    # Standard
    std_embed = StandardEmbedding(vocab_size, d_model)
    t0 = time.time()
    out_std = std_embed(input_ids)
    t_std = time.time() - t0
    
    # Hashed
    hash_embed = HashEmbedding(vocab_size, num_buckets, d_model)
    t0 = time.time()
    out_hash = hash_embed(input_ids)
    t_hash = time.time() - t0
    
    print(f"\n--- Execution Latency ---")
    print(f"1. Standard Embedding : {t_std:.4f}s")
    print(f"2. Hash Embedding     : {t_hash:.4f}s")
    
    print("\n[CHALLENGE RECORDED]:")
    print("Hashing shrinks the first layer memory massively, but multiple unique tokens")
    print("now map to the exact same base vector (Hash Collisions).")
    print("This destroys semantic isolation for rare tokens (e.g., medical terms, specific names).")
    print("Auto-Researcher Goal: Implement 'Multi-Hashing' (e.g., using 2 distinct hashes per token")
    print("and concatenating them) to exponentially reduce collision probability while keeping memory low.")

if __name__ == "__main__":
    simulate_hash_embeddings()