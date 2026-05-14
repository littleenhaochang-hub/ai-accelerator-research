import time

def simulate_dense_attention_prefill(seq_len):
    # O(N^2) time complexity approximation
    return (seq_len ** 2) / 1e9

def simulate_flash_kmeans_attention_prefill(seq_len, num_clusters):
    # O(N * K) time complexity approximation using hardware K-Means engine
    hardware_acceleration_factor = 10.0 # Dedicated distance calculation ALUs
    return ((seq_len * num_clusters) / 1e9) / hardware_acceleration_factor

if __name__ == "__main__":
    seq_len = 131072 # 128K long context
    num_clusters = 512 # K-Means clusters

    dense_time = simulate_dense_attention_prefill(seq_len)
    kmeans_time = simulate_flash_kmeans_attention_prefill(seq_len, num_clusters)
    
    print(f"Dense O(N^2) Prefill Latency: {dense_time:.4f} s")
    print(f"HW-Flash-KMeans O(N*K) Latency: {kmeans_time:.4f} s")
    print(f"Speedup: {dense_time / kmeans_time:.2f}x")
