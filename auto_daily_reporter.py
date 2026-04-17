import os
import re
import datetime
import json
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyAGXn2_QvR2LIlCpJTlltb5TFKTOHSbEfU")
CHECKPOINT_PATH = "/Users/hao/.openclaw/workspace/ai-accelerator-research/RESEARCH_STATUS_CHECKPOINT.md"
REPORT_DIR = "/Users/hao/.openclaw/workspace/ai-accelerator-research/reports"

def get_checkpoint_state():
    if not os.path.exists(CHECKPOINT_PATH): return "無法讀取 Checkpoint。"
    with open(CHECKPOINT_PATH, "r", encoding="utf-8") as f: 
        return f.read()

def fetch_latest_papers():
    # Agentic broad search: Expanded to include pure Model Architecture (SSM, MoE, Mamba) alongside Hardware
    query = urllib.parse.quote('all:"LLM" AND (all:"hardware" OR all:"accelerator" OR all:"architecture" OR all:"quantization" OR all:"attention" OR all:"SSM" OR all:"MoE" OR all:"Mamba" OR "model architecture")')
    url = f"http://export.arxiv.org/api/query?search_query={query}&sortBy=submittedDate&sortOrder=descending&max_results=40"
    try:
        req = urllib.request.urlopen(url)
        xml_data = req.read()
        root = ET.fromstring(xml_data)
        namespace = {'atom': 'http://www.w3.org/2005/Atom'}
        papers = []
        for entry in root.findall('atom:entry', namespace):
            title = entry.find('atom:title', namespace).text.strip().replace('\n', ' ')
            summary = entry.find('atom:summary', namespace).text.strip().replace('\n', ' ')
            link = entry.find('atom:id', namespace).text
            papers.append(f"Title: {title}\nLink: {link}\nSummary: {summary[:400]}...\n")
        return "\n".join(papers)
    except Exception as e:
        return f"Fetch error: {e}"

def generate_report_via_llm(checkpoint_text, papers_text):
    prompt = f"""
    你是一個頂尖的 AI 硬體架構師 (Ghost)。
    請根據我們實驗室的「當前 Checkpoint 狀態」與今天 arXiv 上最新的 40 篇硬體/LLM論文，生成今天的「AI 硬體自動研究晨報」。
    
    【當前實驗室 Checkpoint 狀態 (包含所有 Pillars 與 Baselines)】:
    {checkpoint_text}
    
    【今日 arXiv 最新前沿論文 (Top 40)】:
    {papers_text}
    
    【輸出要求】(必須使用繁體中文，語氣保持 Ghost 的專業、直接、錙銖必較):
    # 🤖 AI 加速器自動研究晨報 (Agentic V2)
    **日期:** {datetime.datetime.now().strftime("%Y-%m-%d")}
    
    ## 🧱 現有支柱文獻對齊 (Pillar Alignment)
    (請動態讀取 Checkpoint 中的 Pillar 標題與內容。將最新的論文精準分配到對應的 Pillar 下，並給出「架構師點評」。
    如果該論文能解決 Checkpoint 中提到的 The Bottleneck，請特別標註！每個 Pillar 最多放 2 篇。若該 Pillar 無進展請寫「維持 Local Baseline 推進」。)
    
    ## 💡 新興趨勢與新支柱提案 (Frontier Discovery)
    (從 40 篇論文中，挑選出「極具顛覆性」但「完全不屬於我們現有 Pillar」的硬體架構論文。
    統整這些新技術，並正式向我提案是否要為其開啟新的 `## Pillar X`。若無具備破壞性創新的論文，可略過此節。)
    """
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.1-pro-preview:generateContent?key={API_KEY}"
    data = {"contents": [{"parts": [{"text": prompt}]}], "generationConfig": {"temperature": 0.2}}
    try:
        req = urllib.request.Request(url, data=json.dumps(data).encode('utf-8'), headers={'Content-Type': 'application/json'})
        with urllib.request.urlopen(req) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            return res['candidates'][0]['content']['parts'][0]['text']
    except Exception as e:
        return f"LLM Error: {e}"

def main():
    os.makedirs(REPORT_DIR, exist_ok=True)
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    
    print("1. Extracting dynamic checkpoint state...")
    checkpoint = get_checkpoint_state()
    
    print("2. Fetching frontier papers from arXiv...")
    papers = fetch_latest_papers()
    
    print("3. Synthesizing report via Agentic LLM...")
    report = generate_report_via_llm(checkpoint, papers)
    
    report_path = os.path.join(REPORT_DIR, f"daily_summary_{date_str}.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Report generated: {report_path}")

if __name__ == "__main__":
    main()
