import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Add a state for debug info
state_patch = """  const [elevationProfile, setElevationProfile] = React.useState<number[] | null>(null);
  const [debugInfo, setDebugInfo] = React.useState<string>('INIT');
"""
content = content.replace("  const [elevationProfile, setElevationProfile] = React.useState<number[] | null>(null);", state_patch)

# Set debug info in updateRouteData
debug_patch = """    if (map.getSource('route')) {
      if (activeMergedCoords.length > 1) {
        (map.getSource('route') as GeoJSONSource).setData({
          type: 'FeatureCollection',
          features: [{
            type: 'Feature',
            properties: {},
            geometry: { type: 'LineString', coordinates: activeMergedCoords }
          }]
        });
      } else {
        (map.getSource('route') as GeoJSONSource).setData({
          type: 'FeatureCollection',
          features: activeFeatures,
        });
      }
    }
    
    setDebugInfo(`Routes: ${_routes.length} | Active: ${activeRouteId} | InactiveFeats: ${inactiveFeatures.length} | Pass: ${passId}`);
"""

content = re.sub(r"    if \(map\.getSource\('route'\)\) \{.*?      \}\n    \}", debug_patch, content, flags=re.DOTALL)

# Render debug info in JSX
jsx_patch = """      {/* Debug Info */}
      <div style={{ position: 'absolute', bottom: 10, left: 10, background: 'rgba(0,0,0,0.8)', color: 'white', padding: '5px', zIndex: 9999, fontSize: '10px' }}>
        {debugInfo}
      </div>
    </div>
  );
}"""

content = content.replace("    </div>\n  );\n}", jsx_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
