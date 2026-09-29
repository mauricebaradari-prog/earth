import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

update_patch = """  async function updateRouteData(map: MaplibreMap, passId: number) {
    try {
      let activeMergedCoords: number[][] = [];
      const inactiveFeatures: GeoJSON.Feature[] = [];
      let activeFeatures: GeoJSON.Feature[] = [];
      const _routes = routes && routes.length > 0 ? routes : ROUTES;
      
      inactiveCoordsRef.current = [];
      fullActiveCoordsRef.current = [];

      for (const r of _routes) {
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
          fullActiveCoordsRef.current = rFeatures;
        } else {
          inactiveFeatures.push(...rFeatures);
          inactiveCoordsRef.current.push({ id: r.id, features: rFeatures });
        }
      }
      
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
      
      setDebugInfo(`Routes: ${_routes.length} | Active: ${activeRouteId} | InactiveFeats: ${inactiveFeatures.length} | Pass: ${passId}`);

      // Update Distance Marker
      let totalPathDist = 0;
      const allSegments: { p1: [number, number]; p2: [number, number]; dist: number }[] = [];
      activeFeatures.forEach((feat) => {
        if (feat.geometry.type === 'LineString') {
          const coords = feat.geometry.coordinates as [number, number][];
          for (let i = 0; i < coords.length - 1; i++) {
            const d = haversineDistance(
              { lat: coords[i][1], lng: coords[i][0], id: '', name: '' },
              { lat: coords[i + 1][1], lng: coords[i + 1][0], id: '', name: '' }
            );
            totalPathDist += d;
            allSegments.push({ p1: coords[i], p2: coords[i + 1], dist: d });
          }
        }
      });
      totalDistRef.current = totalPathDist;

      if (allSegments.length > 0) {
        const targetD = totalPathDist / 2;
        let walkDist = 0;
        let midP: [number, number] | null = null;
        for (let j = 0; j < allSegments.length; j++) {
          const seg = allSegments[j];
          if (walkDist + seg.dist >= targetD) {
            const frac = seg.dist === 0 ? 0 : (targetD - walkDist) / seg.dist;
            midP = [
              seg.p1[0] + (seg.p2[0] - seg.p1[0]) * frac,
              seg.p1[1] + (seg.p2[1] - seg.p1[1]) * frac,
            ];
            break;
          }
          walkDist += seg.dist;
        }
        midLngLatRef.current = midP || allSegments[Math.floor(allSegments.length / 2)].p1;
      }

      if (showElevation && activeFeatures.length > 0) {
        const sampledPts: [number, number][] = [];
        const numSamples = 50;
        for (let i = 0; i <= numSamples; i++) {
          const targetD = (i / numSamples) * totalPathDist;
          let walkDist = 0;
          let found = false;
          for (let j = 0; j < allSegments.length; j++) {
            const seg = allSegments[j];
            if (walkDist + seg.dist >= targetD) {
              const frac = seg.dist === 0 ? 0 : (targetD - walkDist) / seg.dist;
              sampledPts.push([
                seg.p1[0] + (seg.p2[0] - seg.p1[0]) * frac,
                seg.p1[1] + (seg.p2[1] - seg.p1[1]) * frac,
              ]);
              found = true;
              break;
            }
            walkDist += seg.dist;
          }
          if (!found) sampledPts.push(allSegments[allSegments.length - 1].p2);
        }

        const lats = sampledPts.map(p => p[1].toFixed(5)).join(',');
        const lngs = sampledPts.map(p => p[0].toFixed(5)).join(',');
        fetch(`https://api.open-meteo.com/v1/elevation?latitude=${lats}&longitude=${lngs}`)
          .then(r => r.json())
          .then(d => {
            if (d.elevation) setElevationProfile(d.elevation);
          })
          .catch(e => console.error("Elevation fetch failed", e));
      }

      if ((window as any)._updateSvgOverlay) {
        (window as any)._updateSvgOverlay();
      }
    } catch (e: any) {
      setDebugInfo(`ERROR: ${e.message}`);
    }
  }"""

content = re.sub(r'  async function updateRouteData\(map: MaplibreMap, passId: number\) \{.*?    \}\n  \}', update_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
