import os
import glob
import re

html_files = glob.glob('templates/*.html')

for filepath in html_files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # remove onerror fallback
    content = re.sub(r'\s*onerror="this\.src=\'[^\']+\'"', '', content)
    
    # replace hardcoded unsplash images 
    content = re.sub(
        r'src="https://images\.unsplash\.com/[^"]+"',
        r'src="{{ url_for(\'static\', filename=\'images/dashboard_header.png\') }}"',
        content
    )

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("done")
