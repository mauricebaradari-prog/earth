import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Make updateRouteData take passId only
content = content.replace('updateRouteData(map, cities, renderPassRef.current)', 'updateRouteData(map, renderPassRef.current)')

# Redo the replacement manually
match = re.search(r'  async function updateRouteData.*?totalDistRef\.current = totalPathDist;\n  }', content, re.DOTALL)
if match:
    update_route_data_patch = """  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route') || !map.getSource('route-inactive')) return;
    
    let activeMergedCoords: number[][] = [];
    const inactiveFeatures: GeoJSON.Feature[] = [];
    let activeFeatures: GeoJSON.Feature[] = [];

    // Process all routes
    for (const r of routes) {
      const cs = r.cities;
      const rFeatures: GeoJSON.Feature[] = [];
      
      for (let i = 0; i < cs.length - 1; i++) {
        let routeCoords = null;
        try {
          if (renderPassRef.current !== passId) return;
          const cacheKey = `${cs[i].id}-${cs[i+1].id}`;
          if (osrmCacheRef.current[cacheKey]) {
             routeCoords = osrmCacheRef.current[cacheKey];
          } else {
             const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${cs[i].lng},${cs[i].lat};${cs[i+1].lng},${cs[i+1].lat}?geometries=geojson`);
             const data = await res.json();
             if (data.routes && data.routes[0]) {
               routeCoords = data.routes[0].geometry.coordinates;
             }
          }
        } catch (e) {
          console.warn("OSRM fetch failed, using fallback");
        }
        const finalCoords = routeCoords || greatCircleArc(cs[i], cs[i + 1], 120);
        osrmCacheRef.current[`${cs[i].id}-${cs[i+1].id}`] = finalCoords;
        rFeatures.push({
          type: 'Feature',
          properties: { routeId: r.id },
          geometry: { type: 'LineString', coordinates: finalCoords }
        });
      }

      if (r.id === activeRouteId) {
        activeFeatures = rFeatures;
        // Merge active coordinates for gradient
        for (const feat of rFeatures) {
          if (feat.geometry.type === 'LineString') {
            const coords = feat.geometry.coordinates;
            for (let j = 0; j < coords.length; j++) {
              if (j === 0 && activeMergedCoords.length > 0) {
                const last = activeMergedCoords[activeMergedCoords.length - 1];
                if (last[0] === coords[j][0] && last[1] === coords[j][1]) continue;
              }
              activeMergedCoords.push(coords[j]);
            }
          }
        }
      } else {
        inactiveFeatures.push(...rFeatures);
      }
    }

    routeCoordsRef.current = activeFeatures;
    (window as any).__ROUTE_COORDS = activeFeatures;
    
    if (map.getSource('route-inactive')) {
      (map.getSource('route-inactive') as GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: inactiveFeatures,
      });
    }

    if (map.getSource('route')) {
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
    }

    // ── Update Distance Marker ──
    let totalPathDist = 0;
    const allSegments: { p1: [number, number]; p2: [number, number]; dist: number }[] = [];
    
    for (const feat of activeFeatures) {
      if (feat.geometry.type === 'LineString') {
        const coords = feat.geometry.coordinates;
        for (let j = 0; j < coords.length - 1; j++) {
          const d = haversineDistance({ lng: coords[j][0], lat: coords[j][1] }, { lng: coords[j+1][0], lat: coords[j+1][1] });
          totalPathDist += d;
          allSegments.push({ p1: coords[j] as [number, number], p2: coords[j+1] as [number, number], dist: d });
        }
      }
    }

    let midPoint = allSegments.length > 0 ? allSegments[0].p1 : [0, 0];
    let distSoFar = 0;
    const targetDist = totalPathDist / 2;
    for (const seg of allSegments) {
      if (distSoFar + seg.dist >= targetDist) {
        const frac = seg.dist > 0 ? (targetDist - distSoFar) / seg.dist : 0;
        midPoint = [
          seg.p1[0] + (seg.p2[0] - seg.p1[0]) * frac,
          seg.p1[1] + (seg.p2[1] - seg.p1[1]) * frac
        ];
        break;
      }
      distSoFar += seg.dist;
    }
    
    midLngLatRef.current = midPoint as [number, number];
    totalDistRef.current = totalPathDist;
  }"""
    content = content[:match.start()] + update_route_data_patch + content[match.end():]
else:
    print("MATCH FAILED!")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
