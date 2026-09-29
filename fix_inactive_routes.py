import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

init_routes = """  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    if (!map.getSource('route')) {
      map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
    if (!map.getSource('inactive-routes')) {
      map.addSource('inactive-routes', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
    if (!map.getLayer('inactive-routes-line')) {
      map.addLayer({
        id: 'inactive-routes-line',
        type: 'line',
        source: 'inactive-routes',
        layout: {
          'line-join': 'round',
          'line-cap': 'round',
        },
        paint: {
          'line-color': '#ffffff',
          'line-width': width,
          'line-opacity': 0.15,
          'line-dasharray': [2, 2],
        },
      });
    }
  }"""

content = re.sub(
    r'  function initRouteLayers.*?\}\s*\}',
    init_routes,
    content,
    flags=re.DOTALL
)

update_inactive = """  // ── Fetch Inactive Routes ──────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routes || !routeInitializedRef.current) return;
    
    (async () => {
      const allFeatures: GeoJSON.Feature[] = [];
      
      for (const route of routes) {
        // Skip active route
        if (route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id)) {
           continue;
        }
        
        for (let i = 0; i < route.cities.length - 1; i++) {
          const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
          let coords = osrmCacheRef.current[cacheKey];
          
          if (!coords) {
             try {
               const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${route.cities[i].lng},${route.cities[i].lat};${route.cities[i+1].lng},${route.cities[i+1].lat}?geometries=geojson`);
               const data = await res.json();
               if (data.routes && data.routes[0]) {
                 coords = data.routes[0].geometry.coordinates;
                 osrmCacheRef.current[cacheKey] = coords;
               }
             } catch (e) {}
          }
          
          const finalCoords = coords || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
          allFeatures.push({
            type: 'Feature',
            properties: {},
            geometry: { type: 'LineString', coordinates: finalCoords }
          });
        }
      }
      
      if (map.getSource('inactive-routes')) {
        (map.getSource('inactive-routes') as GeoJSONSource).setData({
          type: 'FeatureCollection',
          features: allFeatures,
        });
      }
    })();
  }, [routes, cities, mapStyle]);"""

content = content.replace("  // ── 3. Cities update", update_inactive + "\n\n  // ── 3. Cities update")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
