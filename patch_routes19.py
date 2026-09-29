import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Change FeatureCollection back to Feature for the active route
feature_patch = """    if (map.getSource('route')) {
      if (activeMergedCoords.length > 1) {
        (map.getSource('route') as GeoJSONSource).setData({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: activeMergedCoords }
        });
      } else {
        (map.getSource('route') as GeoJSONSource).setData({
          type: 'FeatureCollection',
          features: activeFeatures,
        });
      }
    }"""

content = re.sub(r"    if \(map\.getSource\('route'\)\) \{.*?      \}\n    \}", feature_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
