import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

satellite_style = """      const styleUrl =
        mapStyle === 'streets'
          ? 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
          : mapStyle === 'terrain'
          ? 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
          : mapStyle === 'satellite'
          ? {
              version: 8,
              sources: {
                'satellite': {
                  type: 'raster',
                  tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
                  tileSize: 256
                }
              },
              layers: [
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
              ]
            }
          : 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';"""

content = content.replace("""      const styleUrl =
        mapStyle === 'streets'
          ? 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
          : mapStyle === 'terrain'
          ? 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
          : 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';""", satellite_style)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
