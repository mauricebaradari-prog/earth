import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Add fullRouteCoordsRef
content = content.replace("const routeCoordsRef = useRef<GeoJSON.Feature[]>([]);", "const routeCoordsRef = useRef<GeoJSON.Feature[]>([]);\n  const fullRouteCoordsRef = useRef<[number, number][]>([]);")

# Populate fullRouteCoordsRef in updateRouteData
update_patch = """    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      fullRouteCoordsRef.current = allCoords;
      if (allCoords.length > 0) {
        midLngLatRef.current = allCoords[Math.floor(allCoords.length / 2)];
      }
    }"""
content = content.replace("""    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      if (allCoords.length > 0) {
        midLngLatRef.current = allCoords[Math.floor(allCoords.length / 2)];
      }
    }""", update_patch)

# Fix updateSvgOverlay to use fullRouteCoordsRef
overlay_patch = """          let fullPts = fullRouteCoordsRef.current;
"""
content = re.sub(r'          let fullPts: \[number, number\]\[\] = \[\];\n          if \(mapRef\.current\.getSource\(\'route\'\)\) \{.*?\n          \}', overlay_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
