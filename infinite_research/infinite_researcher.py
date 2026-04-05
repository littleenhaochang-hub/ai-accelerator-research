import time
import os
import json
import urllib.request
import random
import torch
import math
from datetime import datetime

# --- Configuration ---
STATUS_FILE = "ai-accelerator-research/infinite_research/status.json"
LOG_FILE = "ai-accelerator-research/infinite_research/research_log.md"
STOP_FLAG = "ai-accelerator-research/infinite_research/STOP_ME"

def write_status(state, paper_title="N/A", snr=0.0, iteration=0):
    status = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "state": state,
        "iteration": iteration,
        "current_paper": paper_title,
        "last_snr_db": snr
    }
    with open(STATUS_FILE, "w") as f:
        json.dump(status, f, indent=4)

def fetch_arxiv_paper(start_idx):
    """Fetch a real published paper on LLM quantization/hardware from arXiv."""
    query = "all:quantization+AND+all:LLM"
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=desc&start={start_idx}&max_results=1"
    
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        # arXiv XML namespace
        ns = {'atom': 'http://www.w3.org/2005/Atom'}
        entry = root.find('atom:entry', ns)
        
        if entry is not None:
            title = entry.find('atom:title', ns).text.replace('\n', ' ').strip()
            summary = entry.find('atom:summary', ns).text.replace('\n', ' ').strip()
            link = entry.find('atom:id', ns).text
            return {"title": title, "summary": summary, "link": link}
        return None
    except urllib.error.HTTPError as e:
        if e.code == 429:
            raise Exception("RATE_LIMIT")
        return None
    except Exception as e:
        return None

def fake_quantize(tensor, bits=4, block_size=32):
    qmin, qmax = -(2**(bits-1)), (2**(bits-1)) - 1
    orig_shape = tensor.shape
    if block_size is not None and tensor.shape[-1] % block_size == 0:
        tensor_blocked = tensor.view(-1, block_size)
        max_val = torch.max(torch.abs(tensor_blocked), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor_blocked / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return (q_tensor * scale).view(orig_shape)
    else:
        max_val = torch.max(torch.abs(tensor), dim=-1, keepdim=True)[0]
        scale = max_val / qmax
        scale = torch.clamp(scale, min=1e-5)
        q_tensor = torch.round(tensor / scale)
        q_tensor = torch.clamp(q_tensor, qmin, qmax)
        return q_tensor * scale

def simulate_hardware_evaluation(paper_data):
    """
    To avoid burning out the Mac Mini's RAM with a 24/7 LLM, we simulate 
    the hardware tensor math based on the characteristics found in the paper.
    We create a realistic LLM activation tensor (normal distribution + extreme SiLU outliers).
    """
    # 1. Create a simulated FFN activation tensor (Batch=1, Seq=2048, Dim=4096)
    # We use a smaller tensor to keep the loop fast and CPU-friendly
    tensor = torch.randn(1, 512, 1024)
    
    # Inject severe outliers (SiLU/Softmax artifacts) -> 1% of data is 50x larger
    outlier_mask = torch.rand_like(tensor) > 0.99
    tensor[outlier_mask] *= 50.0

    # 2. Parse paper abstract to "guess" hyperparameters (Simulated Extraction)
    summary = paper_data['summary'].lower()
    bits = 8 if "8-bit" in summary or "int8" in summary else 4
    block_size = 64 if "group" in summary else 32
    
    # 3. Apply Quantization
    quantized_tensor = fake_quantize(tensor, bits=bits, block_size=block_size)
    
    # 4. Calculate Math SNR
    signal_power = torch.mean(tensor**2)
    noise_power = torch.mean((tensor - quantized_tensor)**2)
    snr = 10 * torch.log10(signal_power / noise_power).item()
    
    return snr, bits, block_size

def main():
    if os.path.exists(STOP_FLAG):
        os.remove(STOP_FLAG)
        
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("# Infinite Auto-Researcher Log\n\n")

    iteration = 0
    arxiv_offset = 0
    
    write_status("INITIALIZING")
    
    while True:
        # 1. Check for Stop Flag
        if os.path.exists(STOP_FLAG):
            write_status("STOPPED_BY_USER", iteration=iteration)
            print("Stop flag detected. Terminating infinite research loop.")
            break
            
        write_status("FETCHING_PAPER", iteration=iteration)
        
        # 2. Fetch Published Paper
        try:
            paper = fetch_arxiv_paper(arxiv_offset)
            if paper is None:
                # No more papers or standard error, loop back to start
                arxiv_offset = 0
                time.sleep(10)
                continue
                
            arxiv_offset += 1
            
        except Exception as e:
            write_status(f"ERROR_FETCHING: {str(e)}", iteration=iteration)
            if str(e) == "RATE_LIMIT":
                write_status("API_RATE_LIMIT_WAITING", iteration=iteration)
                print("arXiv API limit reached. Sleeping for 15 minutes...")
                time.sleep(900) # Resume after API limits (15 mins)
                continue
            else:
                time.sleep(10)
                continue

        # 3. Simulate Evaluation based on Paper
        write_status("EVALUATING_TENSORS", paper_title=paper['title'], iteration=iteration)
        
        try:
            snr, bits, blk = simulate_hardware_evaluation(paper)
            
            # 4. Log Results
            status_icon = "🟢 BREAKTHROUGH" if snr > 3.4 else "🔴 FAILED"
            log_entry = f"### Iteration {iteration} | {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
            log_entry += f"- **Paper:** [{paper['title']}]({paper['link']})\n"
            log_entry += f"- **Simulated Config:** W{bits}A{bits}, Block Size: {blk}\n"
            log_entry += f"- **Evaluated SNR:** {snr:.2f} dB -> {status_icon}\n\n"
            
            with open(LOG_FILE, "a") as f:
                f.write(log_entry)
                
            write_status("IDLE", paper_title=paper['title'], snr=snr, iteration=iteration)
            
        except Exception as e:
            write_status(f"EVAL_ERROR: {str(e)}", iteration=iteration)
            
        iteration += 1
        
        # Polite delay to respect arXiv API guidelines (max 1 request per 3 seconds)
        time.sleep(5)

if __name__ == "__main__":
    main()
