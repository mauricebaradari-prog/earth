import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Remove the old distance badge markup
old_badge = r'\{distanceBadge && \(\s*<div\s*className=""\s*style=\{\{.*?\}\}>\s*<div style=\{\{.*?\}\}>\s*<span.*?>\{distanceBadge\.text\}</span>\s*<span.*?>\{distanceBadge\.text2\}</span>\s*</div>\s*</div>\s*\)\}'
content = re.sub(old_badge, '', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
