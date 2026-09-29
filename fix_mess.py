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
        }"""

content = re.sub(r'  function initRouteLayers.*?if \(data\.routes && data\.routes\[0\]\) \{\n             routeCoords = data\.routes\[0\]\.geometry\.coordinates;\n           \}\n        \}', correct_block, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
