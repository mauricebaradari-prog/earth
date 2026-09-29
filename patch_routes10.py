import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("""        (map.getSource('route') as GeoJSONSource).setData({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: activeMergedCoords }
        });""", """        (map.getSource('route') as GeoJSONSource).setData({
          type: 'FeatureCollection',
          features: [{
            type: 'Feature',
            properties: {},
            geometry: { type: 'LineString', coordinates: activeMergedCoords }
          }]
        });""")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
