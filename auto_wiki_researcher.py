import urllib.request
import xml.etree.ElementTree as ET
import os
import json
from datetime import datetime

WIKI_DIR = "/Users/hao/.openclaw/workspace/ai-accelerator-research/wiki"
LOG_FILE = os.path.join(WIKI_DIR, "Meta", "research_log.json")

def fetch_arxiv(query, max_results=3):
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results={max_results}"
    try:
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        entries = root.findall('atom:entry', namespace)
        results = []
        for entry in entries:
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
            published = entry.find('atom:published', namespace).text
            link = entry.find('atom:id', namespace).text
            results.append({"title": title, "published": published, "summary": summary, "link": link})
        return results
    except Exception as e:
        print(f"Error fetching {query}: {e}")
        return []

def load_processed_papers():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return []

def save_processed_paper(link):
    processed = load_processed_papers()
    processed.append(link)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w') as f:
        json.dump(processed, f)

def update_wiki():
    print(f"[{datetime.now().isoformat()}] 啟動 LLM Wiki 知識圖譜自動更新器...")
    processed_links = load_processed_papers()
    
    # Query 1: LUT & Sub-4-bit
    papers = fetch_arxiv("all:LLM+AND+all:hardware+AND+all:LUT", max_results=5)
    for p in papers:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Algorithms_Quantization", "NF4_LUT_Quantization.md")
            append_to_wiki(target_file, p, "LUT & Low-Bit ALU Discoveries")
            save_processed_paper(p["link"])

    # Query 2: Prefill & Sparse
    papers = fetch_arxiv("all:LLM+AND+all:accelerator+AND+all:pruning", max_results=5)
    for p in papers:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Prefill_Sparse_Prediction.md")
            append_to_wiki(target_file, p, "Dynamic Sparse & Prefill Discoveries")
            save_processed_paper(p["link"])
            
    
    # Query 3: Processing in Memory / MoE
    papers = fetch_arxiv("all:LLM+AND+all:accelerator+AND+(all:MoE+OR+all:PIM)", max_results=5)
    for p in papers:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "MoE_Edge_Architecture.md")
            append_to_wiki(target_file, p, "MoE & Near-Memory Accelerators")
            save_processed_paper(p["link"])

    print("Wiki 知識圖譜更新完成。")

def append_to_wiki(filepath, paper_data, section_title):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    content = f"\n## 🤖 Auto-Researcher Update: {datetime.now().strftime('%Y-%m-%d')}\n"
    content += f"### {paper_data['title']}\n"
    content += f"- **發表時間:** {paper_data['published']}\n"
    content += f"- **論文連結:** {paper_data['link']}\n"
    content += f"- **摘要:** {paper_data['summary']}\n\n"
    
    # If file doesn't exist, create it
    if not os.path.exists(filepath):
        with open(filepath, 'w') as f:
            f.write(f"# {section_title}\n")
            
    with open(filepath, 'a') as f:
        f.write(content)
        
    print(f"-> 已將最新研究附加至： {os.path.basename(filepath)}")

if __name__ == "__main__":
    update_wiki()
