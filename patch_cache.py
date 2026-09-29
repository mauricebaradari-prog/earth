import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Initialize osrmCacheRef with localStorage data if available
init_cache = """  const osrmCacheRef = useRef<Record<string, [number, number][]>>({});
  
  useEffect(() => {
    try {
      const stored = localStorage.getItem('osrmCache');
      if (stored) {
        osrmCacheRef.current = JSON.parse(stored);
      }
    } catch(e) {}
  }, []);
  
  const saveOsrmCache = () => {
    try {
      localStorage.setItem('osrmCache', JSON.stringify(osrmCacheRef.current));
    } catch(e) {}
  };
"""

content = content.replace("  const osrmCacheRef = useRef<Record<string, [number, number][]>>({});", init_cache)

# 2. Parallelize the fetches in updateInactiveRoutes and save to cache
old_update = """    for (const route of routes) {
      const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
      if (isActive) continue;
      
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
          } catch(e) {}
        }
        const finalCoords = coords || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        allCoordSegments.push(finalCoords);
        allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: finalCoords }
        });
      }
    }"""

new_update = """    let didFetch = false;
    const fetchPromises = [];

    // First pass: collect missing fetches
    for (const route of routes) {
      const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
      if (isActive) continue;
      for (let i = 0; i < route.cities.length - 1; i++) {
        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        if (!osrmCacheRef.current[cacheKey]) {
          const p = fetch(`https://router.project-osrm.org/route/v1/driving/${route.cities[i].lng},${route.cities[i].lat};${route.cities[i+1].lng},${route.cities[i+1].lat}?geometries=geojson`)
            .then(res => res.json())
            .then(data => {
               if (data.routes && data.routes[0]) {
                 osrmCacheRef.current[cacheKey] = data.routes[0].geometry.coordinates;
                 didFetch = true;
               }
            }).catch(() => {});
          fetchPromises.push(p);
        }
      }
    }
    
    // Wait for all fetches in parallel
    if (fetchPromises.length > 0) {
      await Promise.all(fetchPromises);
      if (didFetch) saveOsrmCache();
    }

    // Second pass: build segments
    for (const route of routes) {
      const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
      if (isActive) continue;
      for (let i = 0; i < route.cities.length - 1; i++) {
        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        const coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        allCoordSegments.push(coords);
        allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: coords }
        });
      }
    }"""

content = content.replace(old_update, new_update)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
