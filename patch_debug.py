import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

debug_inject = """    if (!map.getSource('route') || legDists.length !== cs.length - 1) {
      console.log('Progress abort:', { hasSource: !!map.getSource('route'), legDistsLen: legDists.length, expected: cs.length - 1 });
      return;
    }"""
content = re.sub(r"    if \(!map\.getSource\('route'\) \|\| legDists\.length !== cs\.length - 1\) return;", debug_inject, content)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
