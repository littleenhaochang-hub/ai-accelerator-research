import torch
import sys
import os
import importlib.util

# Load module dynamically because of numeric folder name
spec = importlib.util.spec_from_file_location(
    "sliding_window", 
    "/Users/hao/.openclaw/workspace/ai-accelerator-research/1_model_architecture/1_3_linear_sliding_window/sliding_window.py"
)
sw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sw)

def export_to_onnx():
    print("Initializing Linear Sliding Window Attention...")
    d_model = 256
    window_size = 512
    seq_len = 1024 
    batch = 1
    
    model = sw.LinearSlidingWindowAttention(d_model, window_size)
    model.eval()
    
    dummy_input = torch.randn(batch, seq_len, d_model)
    onnx_path = "/Users/hao/.openclaw/workspace/ai-accelerator-research/1_model_architecture/1_3_linear_sliding_window/sliding_window.onnx"
    
    print(f"Tracing PyTorch graph and exporting to ONNX...")
    torch.onnx.export(
        model, 
        dummy_input, 
        onnx_path, 
        export_params=True,
        opset_version=14,
        do_constant_folding=True,
        input_names=['input_tensor'],
        output_names=['output_tensor'],
        dynamic_axes={'input_tensor': {0: 'batch', 1: 'seq'},
                      'output_tensor': {0: 'batch', 1: 'seq'}}
    )
    print(f"Export successful: {onnx_path}")
    print(f"To finalize TFLite conversion, we need to install `onnx-tf` and `tensorflow`.")

if __name__ == "__main__":
    export_to_onnx()