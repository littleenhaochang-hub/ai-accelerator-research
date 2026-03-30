import torch
import sys
import importlib.util

spec = importlib.util.spec_from_file_location(
    "sliding_window", 
    "/Users/hao/.openclaw/workspace/ai-accelerator-research/1_model_architecture/1_3_linear_sliding_window/sliding_window.py"
)
sw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sw)

def export_tflite():
    print("Initializing Linear Sliding Window Attention for TFLite export...")
    d_model = 256
    window_size = 512
    seq_len = 1024 
    batch = 1
    
    model = sw.LinearSlidingWindowAttention(d_model, window_size)
    model.eval()
    
    sample_input = (torch.randn(batch, seq_len, d_model),)
    tflite_path = "/Users/hao/.openclaw/workspace/ai-accelerator-research/1_model_architecture/1_3_linear_sliding_window/sliding_window.tflite"
    
    print("Tracing PyTorch graph and converting to TFLite via ai-edge-torch...")
    import litert_torch
    edge_model = litert_torch.convert(model, sample_input)
    edge_model.export(tflite_path)
    
    print(f"Export successful: {tflite_path}")

if __name__ == "__main__":
    export_tflite()
