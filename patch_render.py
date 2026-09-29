import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("map.on('render', updateSvgOverlay);", "// map.on('render', updateSvgOverlay); removed to prevent infinite loops")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
