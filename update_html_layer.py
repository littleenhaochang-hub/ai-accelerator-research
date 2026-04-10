import base64
import re

b64_layerwise_path = '/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/real_layerwise_heatmap.png'
with open(b64_layerwise_path, 'rb') as f:
    b64_layerwise_data = base64.b64encode(f.read()).decode('utf-8')

html_path = '/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/gemma4_blueprint_english_with_chart.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

layerwise_section = f"""
<h3>2. Real Per-Layer Gemma-4 26B Profiling</h3>
<p>To provide a true micro-architectural breakdown, we performed a Layer-by-Layer Activation Profiling (60 Layers × 128 Experts). The heatmap below reveals the exact routing density across the entire model depth.</p>
<ul>
<li>🔗 <strong><a href="https://github.com/openclaw/ai-accelerator-research/blob/main/8_structural_sparsity/15_real_layerwise_heatmap.py">Empirical Source Code: Real Per-Layer Gemma-4 26B Profiling</a></strong></li>
</ul>
<p><img src="data:image/png;base64,{b64_layerwise_data}" alt="Real Per-Layer Expert Activation Profiling" style="width:100%; max-width:900px; border-radius:8px; margin: 20px auto; display: block; box-shadow: 0 4px 6px rgba(0,0,0,0.1); border: 1px solid #e5e7eb;"></p>
"""

# Insert it before "<h3>2. Deep Analysis of the Empirical Results</h3>" 
# which is now "<h3>3. Deep Analysis of the Empirical Results</h3>"
html = html.replace('<h3>2. Deep Analysis of the Empirical Results</h3>', layerwise_section + '\n<h3>3. Deep Analysis of the Empirical Results</h3>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
