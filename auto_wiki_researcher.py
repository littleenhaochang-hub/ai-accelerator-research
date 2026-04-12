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
    
    # 搜尋 1: 硬體架構 (Hardware Architecture) - 包含 ISCA, MICRO, arXiv
    papers_hw = fetch_arxiv('all:"hardware architecture"+AND+(all:LLM+OR+all:accelerator)+AND+(all:ISCA+OR+all:MICRO+OR+all:arXiv)', max_results=4)
    for p in papers_hw:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Emerging_Architectures.md")
            append_to_wiki(target_file, p, "硬體架構探索 (Hardware Architecture)")
            save_processed_paper(p["link"])

    # 搜尋 2: 模型架構 (Model Architecture) - 包含 ICML, ICLR, arXiv
    papers_model = fetch_arxiv('all:"model architecture"+AND+(all:LLM+OR+all:SSM+OR+all:MoE)+AND+(all:ICML+OR+all:ICLR+OR+all:arXiv)', max_results=4)
    for p in papers_model:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Model_Architecture_CoDesign.md")
            append_to_wiki(target_file, p, "模型架構與演算法 (Model Architecture)")
            save_processed_paper(p["link"])

    # 搜尋 3: 解決當前瓶頸 (Quantization & Prefill)
    papers_quant = fetch_arxiv('all:quantization+AND+all:LLM+AND+(all:outlier+OR+all:LUT)', max_results=2)
    for p in papers_quant:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Algorithms_Quantization", "NF4_LUT_Quantization.md")
            append_to_wiki(target_file, p, "量化與離群值處理 (Quantization & Outliers)")
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
