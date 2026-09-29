import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("// initRouteLayers(map, routeColor, routeWidth);", "initRouteLayers(map, routeColor, routeWidth);")

# Update initRouteLayers to ONLY add the source, not the layers
init_block = """  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    if (!map.getSource('route')) {
      map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
  }"""

content = re.sub(r'  function initRouteLayers.*?\}\s*\}\s*\}', init_block, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
