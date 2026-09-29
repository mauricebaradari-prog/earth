with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

effect_code = """  // ── 2. Style update ──────────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (map && mapStyle && routeInitializedRef.current) {
      let styleUrl: string | maplibregl.StyleSpecification | undefined = undefined;
      
      if (mapStyle === 'streets') styleUrl = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';
      else if (mapStyle === 'terrain') styleUrl = 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json';
      else if (mapStyle === 'satellite') {
         styleUrl = {
              version: 8 as 8,
              sources: {
                'satellite': {
                  type: 'raster' as 'raster',
                  tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
                  tileSize: 256
                }
              },
              layers: [
                {
                  id: 'background',
                  type: 'background' as 'background',
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
              ]
         };
      } else {
         styleUrl = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';
      }

      map.setStyle(styleUrl);
      map.once('style.load', () => {
        (map as any).setProjection({ type: 'globe' });
        try {
          if (globeAtmosphere && (map as any).setFog) {
             (map as any).setFog({
               color: 'rgba(255, 255, 255, 0.2)',
               'high-color': 'rgba(0, 0, 0, 0.8)',
               'space-color': 'rgba(0, 0, 0, 1)'
             });
          }
        } catch (e) {}

        initRouteLayers(map, routeColor, routeWidth);
        updateRouteData(map, 0); // Reset to full line
        rebuildMarkers(map, cities);
      });
    }
  }, [mapStyle, globeAtmosphere]);\n\n"""

content = content.replace("  // ── Fetch Inactive Routes", effect_code + "  // ── Fetch Inactive Routes")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
