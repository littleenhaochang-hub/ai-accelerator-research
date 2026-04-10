import base64
import re

with open('/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/zipfian_skew_chart.png', 'rb') as f:
    b64_data = base64.b64encode(f.read()).decode('utf-8')

with open('/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/gemma4_blueprint_english_with_chart.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Update texts
html = html.replace('The X-axis ranks the 128 experts from most to least frequently used.', 'The X-axis ranks the 7680 experts (128 experts x 60 layers) from most to least frequently used.')
html = html.replace('128 experts)', '7680 experts)')
html = html.replace('top <strong>42 experts</strong>', 'top <strong>42 experts</strong>') # well maybe keep this as is or adjust it if it means 42 per layer

# Update image
# find <img src="data:image/png;base64,...">
html = re.sub(r'<img src="data:image/png;base64,[^"]+"', f'<img src="data:image/png;base64,{b64_data}"', html)

with open('/Users/hao/.openclaw/workspace/ai-accelerator-research/reports/gemma4_blueprint_english_with_chart.html', 'w', encoding='utf-8') as f:
    f.write(html)
