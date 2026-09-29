import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("""              layers: [
                {
                  id: 'satellite-layer',
                  type: 'raster',
                  source: 'satellite',
                  minzoom: 0,
                  maxzoom: 19
                },
                {
                  id: 'background',
                  type: 'background',
                  paint: {
                    'background-color': '#000000'
                  }
                }
              ]""", """              layers: [
                {
                  id: 'background',
                  type: 'background',
                  paint: {
                    'background-color': '#000000'
                  }
                },
                {
                  id: 'satellite-layer',
                  type: 'raster',
                  source: 'satellite',
                  minzoom: 0,
                  maxzoom: 19
                }
              ]""")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
