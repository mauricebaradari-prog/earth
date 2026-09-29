import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("{ lat: coords[i][1], lng: coords[i][0], id: '', name: '' }", "{ lat: coords[i][1], lng: coords[i][0] }")
content = content.replace("{ lat: coords[i + 1][1], lng: coords[i + 1][0], id: '', name: '' }", "{ lat: coords[i + 1][1], lng: coords[i + 1][0] }")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
