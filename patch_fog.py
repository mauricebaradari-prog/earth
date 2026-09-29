import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'    if \(globeAtmosphere\) \{.*?    \} else \{\n      map\.setFog\(null as any\);\n    \}', '', content, flags=re.DOTALL)
content = re.sub(r'        if \(globeAtmosphere\) \{.*?           \} as any\);\n        \}', '', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
