
import urllib.request
import xml.etree.ElementTree as ET
import os
import json
import re
import subprocess
from datetime import datetime
import google.generativeai as genai

# Setup environment
# Security: Load API key from environment or local .env file, NEVER hardcode in source code
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        env_path = "/Users/hao/.openclaw/workspace/.env"
        if os.path.exists(env_path):
            with open(env_path, "r") as env_f:
                for line in env_f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.split("=")[1].strip().strip("'").strip('"')
                        os.environ['GEMINI_API_KEY'] = api_key
                        break

WIKI_DIR = "/Users/hao/.openclaw/workspace/ai-accelerator-research/wiki"
LOG_FILE = os.path.join(WIKI_DIR, "Meta", "research_log.json")
REPORT_PATH = "/Users/hao/.openclaw/workspace/ai-accelerator-research/RESEARCH_STATUS_CHECKPOINT.md"

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
        with open(LOG_FILE, 'r') as f: return json.load(f)
    return []

def save_processed_paper(link):
    processed = load_processed_papers()
    processed.append(link)
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, 'w') as f: json.dump(processed, f)

def append_to_wiki(filepath, paper_data, section_title):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    content = f"\n## 🤖 Auto-Researcher Update: {datetime.now().strftime('%Y-%m-%d')}\n"
    content += f"### {paper_data['title']}\n"
    content += f"- **發表時間:** {paper_data['published']}\n"
    content += f"- **論文連結:** {paper_data['link']}\n"
    content += f"- **摘要:** {paper_data['summary']}\n\n"
    if not os.path.exists(filepath):
        with open(filepath, 'w', encoding="utf-8") as f: f.write(f"# {section_title}\n")
    with open(filepath, 'a', encoding="utf-8") as f: f.write(content)
    print(f"-> 已將最新研究附加至： {os.path.basename(filepath)}")

def rebuild_wiki_dashboard():
    md_files = []
    for root, _, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md") and file != "Index.md":
                md_files.append(os.path.join(root, file))
    md_files.sort()
    groups = {}
    for f in md_files:
        rel_path = os.path.relpath(f, WIKI_DIR)
        dirname = os.path.dirname(rel_path)
        if dirname not in groups: groups[dirname] = []
        groups[dirname].append((rel_path, f))
        
    index_content = "# 🧠 OpenClaw 硬體與演算法維基總覽 (Auto-Researcher Dashboard)\n\n"
    index_content += "這是由自動研究員 (Auto-Researcher) 自動維護與更新的知識圖譜大廳。所有的研究節點、打樣程式碼與最新論文都會歸檔於下方列表中，點擊連結即可直接閱讀。\n\n"
    
    for folder, files in sorted(groups.items()):
        folder_name = folder.replace("_", " ") if folder else "Root"
        index_content += f"### 📂 {folder_name}\n"
        index_content += "| 檔案連結 (File) | 知識主題 (Topic) | 論文數 | 假說/原型數 |\n"
        index_content += "| :--- | :--- | :---: | :---: |\n"
        for rel_path, full_path in files:
            title = os.path.basename(rel_path).replace(".md", "")
            with open(full_path, "r", encoding="utf-8") as file_obj: text = file_obj.read()
            title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
            if title_match: title = title_match.group(1).strip()
            
            updates = len(re.findall(r'## 🤖 Auto-Researcher', text))
            hyps = len(re.findall(r'## 🧠 Multi-Pillar|## 🧠 Agentic', text))
            protos = len(re.findall(r'## 🧪 Multi-Pillar|## 🧪 Autonomous', text))
            
            papers_str = f"📄 {updates} 篇" if updates > 0 else "-"
            action_str = "-"
            if hyps > 0: action_str = f"🧠 {hyps} 個假說"
            if protos > 0: action_str = f"🧪 {protos} 次打樣"
            if hyps > 0 and protos > 0: action_str = f"🧠 {hyps} 假說, 🧪 {protos} 打樣"
                
            index_content += f"| [`{os.path.basename(rel_path)}`](./{rel_path}) | **{title}** | {papers_str} | {action_str} |\n"
        index_content += "\n"

    with open(os.path.join(WIKI_DIR, "Index.md"), "w", encoding="utf-8") as f: f.write(index_content)
    print("-> 已自動重構 Wiki Dashboard 總覽目錄。")

def run_multi_pillar_agent():
    print(f"\n[{datetime.now().isoformat()}] 啟動 Multi-Pillar Agentic Loop (全領域自主研究)...")
    genai.configure(api_key=os.environ['GEMINI_API_KEY'])
    model = genai.GenerativeModel('gemini-2.5-flash')

    if not os.path.exists(REPORT_PATH): 
        print("找不到 REPORT_PATH")
        return
        
    with open(REPORT_PATH, "r", encoding="utf-8") as f: content = f.read()

    print("-> 正在掃描所有 Pillar 的研究瓶頸...")
    prompt = f"Read this status report:\n{content[-4000:]}\n\nExtract 3 to 4 distinct critical technical bottlenecks from different Pillars. Return a valid JSON array of strings representing these bottlenecks. ONLY output the JSON array, no markdown."
    try:
        resp = model.generate_content(prompt).text.strip()
        if resp.startswith("```json"): resp = resp[7:-3].strip()
        if resp.startswith("```"): resp = resp[3:-3].strip()
        bottlenecks = json.loads(resp)
    except Exception as e:
        print(f"-> 解析瓶頸失敗: {e}，改用 Regex 備用方案")
        bottlenecks = re.findall(r'- \*\*The Bottleneck:\*\* (.*?)\n', content)
        bottlenecks = list(set(bottlenecks))[:4]

    for i, bn in enumerate(bottlenecks):
        print(f"\n{'='*60}")
        print(f"🎯 攻克目標 {i+1}: {bn[:100]}...")
        
        # 1. Explore
        prompt_query = f"Bottleneck: {bn}\n\nGenerate EXACTLY ONE optimal arXiv search query string to find novel solutions (using ONLY keywords and AND/OR operators, no quotes except exact phrases). Example: all:LLM AND all:LUT. ONLY output the query string."
        query = model.generate_content(prompt_query).text.strip().replace('"', '%22').replace(" ", "+")
        print(f"   [探索] arXiv 搜尋條件: {query}")
        
        papers = fetch_arxiv(query, max_results=2)
        paper_context = ""
        if papers:
            print(f"   [探索] 找到 {len(papers)} 篇相關論文。")
            paper_context = "\n\n".join([f"Title: {p['title']}\nSummary: {p['summary']}" for p in papers])
            
            prompt_idea = f"Bottleneck:\n{bn}\n\nNew Papers:\n{paper_context}\n\nTask: Act as an elite AI Hardware Architect. Cross-pollinate the concepts from the new papers with the bottleneck. Propose a highly specific hardware/software co-design hypothesis. Write a 3-paragraph technical hypothesis in Traditional Chinese. Include '假說標題', '原理解析', and '預期 PPA 效益'."
            hypo = model.generate_content(prompt_idea).text.strip()
            
            hypo_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Adversarial_Hypotheses.md")
            if not os.path.exists(hypo_file):
                with open(hypo_file, "w", encoding="utf-8") as f: f.write("# 自主交叉探索與假說生成 (Adversarial Hypotheses)\n")
            with open(hypo_file, "a", encoding="utf-8") as f:
                f.write(f"\n## 🧠 Multi-Pillar 交叉假說: {datetime.now().strftime('%Y-%m-%d')} (目標 {i+1})\n- **攻克瓶頸:** {bn}\n\n{hypo}\n\n---\n")
            print("   [思考] 假說已寫入 Wiki。")
        else:
            print("   [探索] 無相關論文，跳過假說生成。")

        # 2. Prototype
        print("   [打樣] 開始生成 PyTorch 驗證原型碼...")
        prompt_code = f"Bottleneck: {bn}\nIdea Context: {paper_context}\n\nTask: Write a highly specific, standalone PyTorch Python script (max 60 lines) that mathematically prototypes a novel hardware/software co-design solution to this bottleneck. Use random tensors or tiny models. It MUST print a clear 'Verdict' at the end. Output ONLY the raw Python code block."
        code = model.generate_content(prompt_code).text.strip()
        if "```python" in code: code = code.split("```python")[1].split("```")[0].strip()
        elif "```" in code: code = code.split("```")[1].split("```")[0].strip()
            
        script_name = f"auto_prototype_p{i+1}_{datetime.now().strftime('%Y%m%d')}.py"
        script_path = os.path.join("/Users/hao/.openclaw/workspace/ai-accelerator-research", script_name)
        with open(script_path, "w", encoding="utf-8") as f: f.write(code)
        
        print(f"   [執行] 正在背景執行 {script_name} ...")
        try:
            python_bin = "/Users/hao/.openclaw/workspace/venv/bin/python"
            result = subprocess.run([python_bin, script_path], capture_output=True, text=True, timeout=60)
            output = result.stdout + "\n" + result.stderr
        except Exception as e:
            output = str(e)
            
        proto_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Autonomous_Prototypes.md")
        if not os.path.exists(proto_file):
            with open(proto_file, "w", encoding="utf-8") as f: f.write("# 自主打樣與驗證日誌 (Autonomous Prototypes)\n")
        with open(proto_file, "a", encoding="utf-8") as f:
            f.write(f"\n## 🧪 Multi-Pillar 自主打樣: {datetime.now().strftime('%Y-%m-%d')} (目標 {i+1})\n- **Target Bottleneck:** {bn}\n- **Script Generated:** `{script_name}`\n- **Execution Output / Verdict:**\n```text\n{output[:1500]}\n```\n---\n")
        print("   [完成] 原型驗證結果已寫入 Wiki。")

def update_wiki():
    print(f"[{datetime.now().isoformat()}] 啟動 LLM Wiki 知識圖譜自動更新器 (Static Crawlers)...")
    processed_links = load_processed_papers()
    
    # 靜態爬蟲 (硬體、模型、量化、盲測)
    queries = [
        ('all:%22hardware+architecture%22+AND+(all:LLM+OR+all:accelerator)+AND+(all:ISCA+OR+all:MICRO+OR+all:arXiv)', "Emerging_Architectures.md", "硬體架構探索"),
        ('all:%22model+architecture%22+AND+(all:LLM+OR+all:SSM+OR+all:MoE)+AND+(all:ICML+OR+all:ICLR+OR+all:arXiv)', "Model_Architecture_CoDesign.md", "模型架構與演算法"),
        ('all:quantization+AND+all:LLM+AND+(all:outlier+OR+all:LUT)', "NF4_LUT_Quantization.md", "量化與離群值處理"),
        ('all:%22hardware+accelerator%22+AND+all:%22beyond+CMOS%22', "Wildcard_Exploration.md", "未知領域盲測")

        ('all:QAT+AND+all:%22Quantization-Aware+Training%22+AND+(all:LLM+OR+all:transformer)+AND+(all:%221.58-bit%22+OR+all:ternary+OR+all:%222-bit%22)', "QAT_Extreme_LowBit.md", "量化感知訓練與極端低位元適應 (QAT & 2-bit)"),
    ]
    
    for q, filename, title in queries:
        papers = fetch_arxiv(q, max_results=3)
        for p in papers:
            if p["link"] not in processed_links:
                target = os.path.join(WIKI_DIR, "Hardware_Architecture" if "Architecture" in filename or "Wildcard" in filename else "Algorithms_Quantization", filename)
                append_to_wiki(target, p, title)
                save_processed_paper(p["link"])

    # 啟動全領域自主研究
    run_multi_pillar_agent()
    rebuild_wiki_dashboard()
    print("\n🎉 系統維護完成！")

if __name__ == "__main__":
    update_wiki()
