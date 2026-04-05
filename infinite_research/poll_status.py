import json
import os

STATUS_FILE = "ai-accelerator-research/infinite_research/status.json"

if os.path.exists(STATUS_FILE):
    with open(STATUS_FILE, "r") as f:
        data = json.load(f)
    print(f"🤖 Auto-Researcher Status:")
    print(f"   State:     {data.get('state')}")
    print(f"   Iteration: {data.get('iteration')}")
    print(f"   Paper:     {data.get('current_paper')}")
    print(f"   Last SNR:  {data.get('last_snr_db'):.2f} dB")
    print(f"   Updated:   {data.get('timestamp')}")
else:
    print("Status file not found. Process may not be running.")
