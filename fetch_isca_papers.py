import urllib.request
import xml.etree.ElementTree as ET

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

print("=== Sub-4-bit / LUT ALU Accelerators ===")
lut_papers = fetch_arxiv("all:LLM+AND+all:hardware+AND+all:LUT", max_results=2)
for p in lut_papers:
    print(f"- Title: {p['title']}\n  Date: {p['published']}\n  Link: {p['link']}\n  Summary: {p['summary'][:300]}...\n")

print("=== Dynamic Token Pruning / MoE Hardware ===")
prune_papers = fetch_arxiv("all:LLM+AND+all:accelerator+AND+all:pruning", max_results=2)
for p in prune_papers:
    print(f"- Title: {p['title']}\n  Date: {p['published']}\n  Link: {p['link']}\n  Summary: {p['summary'][:300]}...\n")

print("=== ISCA / MICRO Specific Accelerators ===")
isca_papers = fetch_arxiv("all:ISCA+AND+all:LLM+AND+all:accelerator", max_results=2)
for p in isca_papers:
    print(f"- Title: {p['title']}\n  Date: {p['published']}\n  Link: {p['link']}\n  Summary: {p['summary'][:300]}...\n")
