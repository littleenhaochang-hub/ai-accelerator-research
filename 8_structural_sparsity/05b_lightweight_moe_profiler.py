import torch
import collections
from transformers import AutoModelForCausalLM, AutoTokenizer
import numpy as np

# We'll use a tiny model to test the profiling logic, or just explain the OOM
print("Script execution started...")
