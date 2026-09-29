import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("(map as any).setProjection({ type: 'globe' });", "// (map as any).setProjection({ type: 'globe' });")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
