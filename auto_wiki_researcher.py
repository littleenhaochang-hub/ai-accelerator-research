import re
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



def run_autonomous_prototyper(model):
    print(f"[{datetime.now().isoformat()}] 啟動 Autonomous Prototyper (問題分析與解法實作)...")
    
    # 1. Read current bottlenecks
    report_path = "/Users/hao/.openclaw/workspace/ai-accelerator-research/RESEARCH_STATUS_CHECKPOINT.md"
    if not os.path.exists(report_path):
        print("-> 找不到 RESEARCH_STATUS_CHECKPOINT.md")
        return
        
    with open(report_path, "r", encoding="utf-8") as f:
        report_content = f.read()
        
    # Extract the most recent bottleneck
    bottlenecks = re.findall(r'- \*\*The Bottleneck:\*\*(.*?)(?=- \*\*|$)', report_path, re.DOTALL | re.IGNORECASE)
    # Actually let's just ask the LLM to find the most pressing bottleneck from the whole text
    
    prompt_extract = f"As an AI Hardware Architect, read this status report:\n{report_content[-3000:]}\n\nIdentify the SINGLE most critical unresolved technical bottleneck (e.g., a specific quantization failure or memory bandwidth issue). Summarize the bottleneck in one sentence."
    bottleneck_summary = model.generate_content(prompt_extract).text.strip()
    print(f"-> 鎖定核心瓶頸: {bottleneck_summary}")
    
    # 2. Design a PyTorch Prototype Solution
    prompt_code = f"Bottleneck: {bottleneck_summary}\n\nTask: Write a highly specific, standalone PyTorch Python script (max 60 lines) that mathematically prototypes a novel hardware/software co-design solution to this bottleneck. Use a random tensor or a very small proxy model (like Qwen 0.5B via transformers if absolutely necessary, but prefer random tensors for speed) to prove the math (e.g., calculate SQNR or FLOPs reduction). The script MUST print a clear 'Verdict' at the end. Output ONLY the raw Python code block, no markdown formatting around it if possible, or just standard ```python block."
    
    code_response = model.generate_content(prompt_code).text.strip()
    
    # Extract code from markdown if present
    if "```python" in code_response:
        code = code_response.split("```python")[1].split("```")[0].strip()
    elif "```" in code_response:
        code = code_response.split("```")[1].split("```")[0].strip()
    else:
        code = code_response
        
    script_name = f"auto_prototype_{datetime.now().strftime('%Y%m%d')}.py"
    script_path = os.path.join("/Users/hao/.openclaw/workspace/ai-accelerator-research", script_name)
    
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"-> 已生成原型腳本: {script_name}")
    
    # 3. Execute the Prototype
    import subprocess
    print(f"-> 執行原型驗證中...")
    try:
        # Use the venv python
        python_bin = "/Users/hao/.openclaw/workspace/venv/bin/python"
        result = subprocess.run([python_bin, script_path], capture_output=True, text=True, timeout=120)
        output = result.stdout + "\n" + result.stderr
        print("-> 執行完畢。")
    except subprocess.TimeoutExpired:
        output = "Execution timed out."
        print("-> 執行超時。")
    except Exception as e:
        output = str(e)
        print("-> 執行失敗。")
        
    # 4. Report the findings
    target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Autonomous_Prototypes.md")
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    log_entry = f"\n## 🧪 Autonomous Prototype: {datetime.now().strftime('%Y-%m-%d')}\n"
    log_entry += f"- **Target Bottleneck:** {bottleneck_summary}\n"
    log_entry += f"- **Script Generated:** `{script_name}`\n"
    log_entry += f"- **Execution Output / Verdict:**\n```text\n{output[:1500]}\n```\n---\n"
    
    if not os.path.exists(target_file):
        with open(target_file, 'w', encoding="utf-8") as f:
            f.write("# 自主打樣與驗證日誌 (Autonomous Prototypes)\n")
            
    with open(target_file, 'a', encoding="utf-8") as f:
        f.write(log_entry)
        
    print("-> 原型驗證結果已寫入 Autonomous_Prototypes.md")

def run_agentic_exploration():
    import google.generativeai as genai
    import os
    os.environ.setdefault('GEMINI_API_KEY', 'AIzaSyAGXn2_QvR2LIlCpJTlltb5TFKTOHSbEfU')

    print(f"[{datetime.now().isoformat()}] 啟動 Agentic LLM 交叉探索 (Adversarial Idea Generation)...")
    
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("未設定 GEMINI_API_KEY，略過 Agentic 探索。")
        return
        
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.5-flash')
    run_autonomous_prototyper(model)
    
    # 1. Read current bottleneck
    report_path = "/Users/hao/.openclaw/workspace/RESEARCH_REPORT.md"
    bottleneck_text = "Unknown"
    if os.path.exists(report_path):
        with open(report_path, "r", encoding="utf-8") as f:
            bottleneck_text = f.read()[-2000:] # read the end of report for latest bottlenecks
            
    # 2. Generate custom arXiv queries
    prompt_query = f"Based on the following research status:\n{bottleneck_text}\n\nGenerate EXACTLY ONE optimal arXiv search query string to find novel solutions (using only keywords and AND/OR operators, no quotes except for exact phrases, must include LLM or neural). Example: all:LLM AND all:LUT. ONLY output the query string."
    
    response = model.generate_content(prompt_query)
    custom_query = response.text.strip().replace('"', '%22').replace(" ", "+")
    
    print(f"-> Agent 生成自訂搜尋條件: {custom_query}")
    papers = fetch_arxiv(custom_query, max_results=3)
    
    if not papers:
        print("-> 找不到相符論文。")
        return
        
    # 3. Cross-Pollination Hypothesis
    paper_summaries = "\n\n".join([f"Title: {p['title']}\nSummary: {p['summary']}" for p in papers])
    prompt_idea = f"Research Bottlenecks:\n{bottleneck_text}\n\nNew Papers Found:\n{paper_summaries}\n\nTask: Act as an elite AI Hardware Architect. Cross-pollinate the concepts from the new papers with our current bottlenecks. Propose a highly specific, novel hardware/software co-design hypothesis (e.g., combining two distinct methods). Write a 3-paragraph technical hypothesis in Traditional Chinese. Include '假說標題' (Hypothesis Title), '原理解析' (Mechanism), and '預期 PPA 效益' (Expected PPA)."
    
    idea_response = model.generate_content(prompt_idea)
    hypothesis = idea_response.text.strip()
    
    # 4. Save to Wiki
    target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Adversarial_Hypotheses.md")
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    content = f"\n## 🧠 Agentic 交叉探索假說: {datetime.now().strftime('%Y-%m-%d')}\n"
    content += f"- **觸發關鍵字:** `{custom_query}`\n"
    content += f"\n{hypothesis}\n\n---\n"
    
    if not os.path.exists(target_file):
        with open(target_file, 'w', encoding="utf-8") as f:
            f.write("# 自主交叉探索與假說生成 (Adversarial Hypotheses)\n")
            
    with open(target_file, 'a', encoding="utf-8") as f:
        f.write(content)
        
    print("-> 假說生成完成，已寫入 Adversarial_Hypotheses.md")


def rebuild_wiki_dashboard():
    import re
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
        if dirname not in groups:
            groups[dirname] = []
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
            with open(full_path, "r", encoding="utf-8") as file_obj:
                text = file_obj.read()
            title_match = re.search(r'^#\s+(.+)$', text, re.MULTILINE)
            if title_match: title = title_match.group(1).strip()
            
            updates = len(re.findall(r'## 🤖 Auto-Researcher', text))
            hyps = len(re.findall(r'## 🧠 Agentic 交叉探索假說', text))
            protos = len(re.findall(r'## 🧪 Autonomous Prototype', text))
            
            papers_str = f"📄 {updates} 篇" if updates > 0 else "-"
            action_str = "-"
            if hyps > 0: action_str = f"🧠 {hyps} 個假說"
            if protos > 0: action_str = f"🧪 {protos} 次打樣"
            if hyps > 0 and protos > 0: action_str = f"🧠 {hyps} 假說, 🧪 {protos} 打樣"
                
            index_content += f"| [`{os.path.basename(rel_path)}`](./{rel_path}) | **{title}** | {papers_str} | {action_str} |\n"
            
        index_content += "\n"

    with open(os.path.join(WIKI_DIR, "Index.md"), "w", encoding="utf-8") as f:
        f.write(index_content)
    print("-> 已自動重構 Wiki Dashboard 總覽目錄。")

def update_wiki():
    print(f"[{datetime.now().isoformat()}] 啟動 LLM Wiki 知識圖譜自動更新器...")
    processed_links = load_processed_papers()
    
    # 搜尋 1: 硬體架構 (Hardware Architecture) - 包含 ISCA, MICRO, arXiv
    papers_hw = fetch_arxiv('all:%22hardware+architecture%22+AND+(all:LLM+OR+all:accelerator)+AND+(all:ISCA+OR+all:MICRO+OR+all:arXiv)', max_results=4)
    for p in papers_hw:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Emerging_Architectures.md")
            append_to_wiki(target_file, p, "硬體架構探索 (Hardware Architecture)")
            save_processed_paper(p["link"])

    # 搜尋 2: 模型架構 (Model Architecture) - 包含 ICML, ICLR, arXiv
    papers_model = fetch_arxiv('all:%22model+architecture%22+AND+(all:LLM+OR+all:SSM+OR+all:MoE)+AND+(all:ICML+OR+all:ICLR+OR+all:arXiv)', max_results=4)
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
            
    
    # 搜尋 4: 未知領域盲測 (Wildcard Exploration)
    # 用途：探索完全不在預期內的新技術名詞 (例如光子計算、生物運算、或是全新的硬體詞彙)
    papers_wild = fetch_arxiv('all:%22hardware+accelerator%22+AND+all:%22beyond+CMOS%22', max_results=2)
    for p in papers_wild:
        if p["link"] not in processed_links:
            target_file = os.path.join(WIKI_DIR, "Hardware_Architecture", "Wildcard_Exploration.md")
            append_to_wiki(target_file, p, "未知領域盲測 (Wildcard Exploration)")
            save_processed_paper(p["link"])

    run_agentic_exploration()
    rebuild_wiki_dashboard()
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
