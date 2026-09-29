import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("const pts = [];", "const pts: string[] = [];")
content = content.replace("const p = mapRef.current.project([c[0], c[1]]);", "if (!mapRef.current) continue;\n                 const p = mapRef.current.project([c[0], c[1]]);")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
