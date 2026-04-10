import re

path = '/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/gemma4_blueprint_english_with_chart.html'

with open(path, 'r', encoding='utf-8') as f:
    html = f.read()

# Add model spec to Section 1
spec_html = """<h2>🚀 I. Physical Micro-Architecture Teardown of Gemma-4 26B A4B</h2>
<h3>Model Specification Overview</h3>
<ul>
<li><strong>Total Parameters:</strong> 26 Billion</li>
<li><strong>Layers:</strong> 60 Transformer Blocks</li>
<li><strong>Experts per Layer:</strong> 128 Experts (MoE Routing)</li>
<li><strong>Total Experts:</strong> 7680 Experts System-Wide (60 layers × 128)</li>
<li><strong>Active Parameters per Token:</strong> ~2.4B Active Parameters</li>
<li><strong>Quantization:</strong> A8KV8 (K), FP4 (V/Weights/Activations), E4M3 Scales</li>
</ul>
"""

html = re.sub(r'<h2>🚀 I\. Physical Micro-Architecture Teardown of Gemma-4 26B A4B</h2>', spec_html, html)

# Ensure Section 2 mentions Real Profiling and 128*60 experts
html = html.replace('128 experts (the red bars)', '42 experts per layer (the red bars)')
html = html.replace('128 experts from most to least frequently used', '7680 experts (128 experts x 60 layers) from most to least frequently used')

with open(path, 'w', encoding='utf-8') as f:
    f.write(html)
