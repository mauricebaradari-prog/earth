import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("map.setPaintProperty('route-glow', 'line-gradient', gradient);", "map.setPaintProperty('route-glow', 'line-gradient', gradient as any);")
content = content.replace("map.setPaintProperty('route-line', 'line-gradient', gradient);", "map.setPaintProperty('route-line', 'line-gradient', gradient as any);")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
