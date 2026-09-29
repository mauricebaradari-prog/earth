import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

correct_block = """  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    if (!map.getSource('route')) {
      map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
  }

  // ── 3. Cities update ─────────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    renderPassRef.current += 1;
    updateRouteData(map, renderPassRef.current);
    rebuildMarkers(map, cities);

    if (cities.length >= 2) {
      const lats = cities.map((c) => c.lat);
      const lngs = cities.map((c) => c.lng);
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLng = Math.min(...lngs);
      const maxLng = Math.max(...lngs);
      map.fitBounds(
        [
          [minLng, minLat],
          [maxLng, maxLat],
        ],
        { padding: 100, duration: 1200 }
      );
    }
  }, [cities]);

  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route')) return;
    
    let totalPathDist = 0;
    const lDists: number[] = [];
    const allFeatures: GeoJSON.Feature[] = [];

    for (let i = 0; i < cities.length - 1; i++) {
      let routeCoords = null;
      try {
        if (renderPassRef.current !== passId) return;
        const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
        if (osrmCacheRef.current[cacheKey]) {
           routeCoords = osrmCacheRef.current[cacheKey];
        } else {
           const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`);
           const data = await res.json();
           if (data.routes && data.routes[0]) {
             routeCoords = data.routes[0].geometry.coordinates;
           }
        }
      } catch (e) {
        console.warn("OSRM fetch failed, using fallback");
      }

      const finalCoords = routeCoords || greatCircleArc(cities[i], cities[i + 1], 120);
      osrmCacheRef.current[`${cities[i].id}-${cities[i+1].id}`] = finalCoords;

      let legDist = 0;
      for (let j = 0; j < finalCoords.length - 1; j++) {
        legDist += distance(finalCoords[j], finalCoords[j+1]);
      }
      lDists.push(legDist);
      totalPathDist += legDist;

      allFeatures.push({
        type: 'Feature',
        properties: {},
        geometry: { type: 'LineString', coordinates: finalCoords }
      });
    }

    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      fullRouteCoordsRef.current = allCoords;
      if (allCoords.length > 0) {
        midLngLatRef.current = allCoords[Math.floor(allCoords.length / 2)];
      }
    }
    
    totalDistRef.current = totalPathDist;
    legDistancesRef.current = lDists;
    
    if (map.getSource('route')) {
      (map.getSource('route') as GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: allFeatures,
      });
    }
    
    // Fetch elevation profile
    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      const sampledPts = [];
      const numSamples = 60;
      for (let i = 0; i < numSamples; i++) {
        const idx = Math.floor((i / (numSamples - 1)) * (allCoords.length - 1));
        sampledPts.push(allCoords[idx]);
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

    updateRouteProgress(map, cities, animationProgress, totalPathDist, lDists);
  }

  function updateRouteProgress("""

content = re.sub(
    r'  function initRouteLayers.*?function updateRouteProgress\(',
    correct_block + '(',
    content,
    flags=re.DOTALL
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
