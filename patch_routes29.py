import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = re.sub(r"    if \(!map\.getSource\('route'\) \|\| !map\.getSource\('route-inactive'\)\) return;\n\s*", "", content)
content = re.sub(r"    if \(!map\.getSource\('route'\)\) return;\n\s*", "", content)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
