import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

init_patch = """  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    // No MapLibre layers for routes anymore, everything is handled by SVG perfectly!
  }"""

content = re.sub(r'  function initRouteLayers\(map: MaplibreMap, color: string, width: number\) \{.*?  \}', init_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
