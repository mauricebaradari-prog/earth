import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_active = """    for (let i = 0; i < cities.length - 1; i++) {
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
    }"""

new_active = """    let didFetch = false;
    const fetchPromises = [];
    
    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      if (!osrmCacheRef.current[cacheKey]) {
        const p = fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`)
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

    if (fetchPromises.length > 0) {
      await Promise.all(fetchPromises);
      if (didFetch) saveOsrmCache();
    }

    if (renderPassRef.current !== passId) return;

    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      const finalCoords = osrmCacheRef.current[cacheKey] || greatCircleArc(cities[i], cities[i + 1], 120);
      osrmCacheRef.current[cacheKey] = finalCoords;

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
    }"""

content = content.replace(old_active, new_active)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
