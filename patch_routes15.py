import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("          'line-opacity': 0.3,\n          'line-color': '#FFFFFF'", "          'line-opacity': 1,\n          'line-color': '#FF0000'")
content = content.replace("          'line-opacity': 0.7,\n          'line-color': '#FFFFFF'", "          'line-opacity': 1,\n          'line-color': '#FF0000'")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
