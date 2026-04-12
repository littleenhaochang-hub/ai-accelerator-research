
def extract_autonomous_prototypes():
    target_file = "/Users/hao/.openclaw/workspace/ai-accelerator-research/wiki/Hardware_Architecture/Autonomous_Prototypes.md"
    if not os.path.exists(target_file):
        return ""
        
    with open(target_file, "r", encoding="utf-8") as f:
        content = f.read()
        
    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
    if today_str not in content:
        return "\n*今日 Autonomous Prototyper 無新增打樣測試。*\n"
        
    # Extract only today's section
    import re
    matches = re.findall(r'## 🧪 Autonomous Prototype: ' + today_str + r'.*?(?=\n## 🧪|$)', content, re.DOTALL)
## 🧪 Autonomous Prototype:|\Z)', content, re.DOTALL)
    
    if not matches:
        return "\n*今日 Autonomous Prototyper 無新增打樣測試。*\n"
        
    report = "\n## 🧪 AI 自主打樣與驗證報告 (Autonomous Prototyper)\n"
    for match in matches:
        # Format the output a bit cleaner for the daily report
        report += match + "\n"
        
    return report


def extract_wiki_updates():
    wiki_dir = "/Users/hao/.openclaw/workspace/ai-accelerator-research/wiki"
    wiki_report = "\n## 🤖 Auto-Researcher 論文探索總結 (今日最新)\n"
    
    found_updates = False
    
    if not os.path.exists(wiki_dir):
        return ""
        
    for root, _, files in os.walk(wiki_dir):
        for file in files:
            if not file.endswith(".md"): continue
            
            filepath = os.path.join(root, file)
            with open(filepath, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            in_update = False
            update_text = ""
            for line in lines:
                if line.startswith("## 🤖 Auto-Researcher"):
                    # Check if it's today
                    today_str = datetime.datetime.now().strftime('%Y-%m-%d')
                    if today_str in line:
                        in_update = True
                        found_updates = True
                        wiki_report += f"\n### 📂 分類: {file.replace('.md', '')}\n"
                        continue
                    else:
                        in_update = False
                        
                if in_update:
                    if line.startswith("### "):
                        wiki_report += f"- **論文標題:** {line.replace('### ', '').strip()}\n"
                    elif line.startswith("- **摘要:**"):
                        wiki_report += f"  - **重點:** {line.replace('- **摘要:**', '').strip()[:200]}...\n"
                    elif line.startswith("- **Link:**") or line.startswith("- **論文連結:**"):
                        wiki_report += f"  - **連結:** {line.replace('- **論文連結:**', '').replace('- **Link:**', '').strip()}\n"

    if not found_updates:
        wiki_report += "\n*今日 Auto-Researcher 無新增文獻或探索紀錄。*\n"
        
    return wiki_report

import datetime
import os
import re

REPORT_TEMPLATE = """# AI 加速器自動研究系統 (Auto-Researcher) 每日總結報表
**日期:** {date}

本報表彙整了 `ai-accelerator-research` 儲存庫中，所有活躍研究支柱 (Research Pillars) 的目前狀態、最新突破與下一步行動。

{content}
"""

def extract_pillars(checkpoint_path="/Users/hao/.openclaw/workspace/ai-accelerator-research/RESEARCH_STATUS_CHECKPOINT.md"):
    if not os.path.exists(checkpoint_path):
        return "錯誤：找不到 RESEARCH_STATUS_CHECKPOINT.md"
        
    with open(checkpoint_path, "r") as f:
        content = f.read()
        
    # Split by Pillar
    pillars = re.split(r'## Pillar \d+:', content)
    if len(pillars) < 2:
        return "錯誤：無法解析研究支柱 (Pillars)"
        
    report_body = ""
    
    for i, pillar_text in enumerate(pillars[1:], 1):
        # Extract Pillar Name
        first_line = pillar_text.split('\n')[0].strip()
        report_body += f"\n## 🧱 支柱 {i}: {first_line}\n"
        
        # Extract Sub-Pillars
        sub_pillars = re.split(r'### \d+\.\d+', pillar_text)
        
        for j, sub_text in enumerate(sub_pillars[1:], 1):
            lines = sub_text.strip().split('\n')
            if not lines: continue
            
            title_match = re.match(r'(.*?)\(`(.*?)`\)', lines[0])
            title = lines[0].strip()
            script_link = ""
            
            if "`" in title:
                parts = title.split("`")
                title = parts[0].strip()
                script_link = f"`{parts[1]}`"
            
            script_matches = re.search(r'\[Scripts:(.*?)\]', sub_text)
            if script_matches:
                script_link = f"`{script_matches.group(1).strip()}`"

            status = ""
            findings = ""
            next_steps = ""
            
            for line in lines[1:]:
                if line.startswith("- **Status:**"): status = line.replace("- **Status:**", "").strip()
                elif line.startswith("- **Findings:**") or line.startswith("- **Methodology") or "Breakthrough" in line:
                    findings += line.replace("- **Findings:**", "").strip() + " "
                elif line.startswith("- **Next Steps:**") or line.startswith("- **The Fix") or line.startswith("- **The Bottleneck"):
                    next_steps += line.strip() + " "
            
            report_body += f"### {i}.{j} {title}\n"
            if script_link: report_body += f"- **原始碼:** {script_link}\n"
            if status: report_body += f"- **目前狀態:** {status}\n"
            if findings: report_body += f"- **核心發現:** {findings[:150]}...\n"
            if next_steps: report_body += f"- **瓶頸與下一步:** {next_steps[:150]}...\n"
            
    return report_body

def generate_report():
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    content = extract_pillars()
    wiki_content = extract_wiki_updates()
    proto_content = extract_autonomous_prototypes()
    content = wiki_content + "\n\n---\n" + proto_content + "\n\n---\n" + content
    full_report = REPORT_TEMPLATE.format(date=date_str, content=content)
    
    os.makedirs("/Users/hao/.openclaw/workspace/ai-accelerator-research/reports", exist_ok=True)
    report_path = f"/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/daily_summary_{date_str}.md"
    
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(full_report)
        
    print(f"每日硬體研究報表已生成於 {report_path}")
    return report_path, full_report

if __name__ == "__main__":
    generate_report()
