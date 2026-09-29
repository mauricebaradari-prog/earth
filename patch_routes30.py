import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace from function initRouteLayers to the end of the function (which is before function updateRouteData)
init_patch = """  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    // No MapLibre layers for routes anymore, everything is handled by SVG perfectly!
  }"""

content = re.sub(r'  function initRouteLayers\(map: MaplibreMap, color: string, width: number\) \{.*?(?=  async function updateRouteData)', init_patch + '\n\n', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
