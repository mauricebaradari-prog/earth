import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("          'line-opacity': 1,\n          'line-color': '#FF0000'", "          'line-opacity': 0.4,\n          'line-color': '#FFFFFF'")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
