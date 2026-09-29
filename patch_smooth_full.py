import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Make sure we smooth the combined route points, not just segment by segment!
old_inactive = """    // Second pass: build segments
    for (const route of routes) {
      const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
      if (isActive) continue;
      for (let i = 0; i < route.cities.length - 1; i++) {
        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        const coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        const finalCoords = route.forceStraight ? smoothCoords(coords, 3) : coords;
        allCoordSegments.push(finalCoords);
        allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: finalCoords }
        });
      }
    }"""

new_inactive = """    // Second pass: build segments
    for (const route of routes) {
      const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
      if (isActive) continue;
      
      let routeFullCoords: [number, number][] = [];
      for (let i = 0; i < route.cities.length - 1; i++) {
        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        let coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        if (i > 0 && coords.length > 0) coords = coords.slice(1); // avoid duplicate joints
        routeFullCoords.push(...coords);
      }
      
      if (route.forceStraight) {
          routeFullCoords = smoothCoords(routeFullCoords, 3);
      }
      
      allCoordSegments.push(routeFullCoords);
      allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: routeFullCoords }
      });
    }"""

content = content.replace(old_inactive, new_inactive)


old_active = """    if (renderPassRef.current !== passId) return;

    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      let finalCoords = osrmCacheRef.current[cacheKey] || greatCircleArc(cities[i], cities[i + 1], 120);
      if (activeRoute?.forceStraight) {
        finalCoords = smoothCoords(finalCoords, 3);
      }
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

new_active = """    if (renderPassRef.current !== passId) return;

    let routeFullCoords: [number, number][] = [];
    const segmentIndices: number[] = [0];

    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      let coords = osrmCacheRef.current[cacheKey] || greatCircleArc(cities[i], cities[i + 1], 120);
      osrmCacheRef.current[cacheKey] = coords; // cache original
      if (i > 0 && coords.length > 0) coords = coords.slice(1);
      routeFullCoords.push(...coords);
      segmentIndices.push(routeFullCoords.length - 1);
    }

    if (activeRoute?.forceStraight) {
      routeFullCoords = smoothCoords(routeFullCoords, 3);
      // Re-map segment distances roughly (smoothing shrinks distance slightly, but close enough for animation)
    }

    // Now reconstruct lDists
    for (let i = 0; i < segmentIndices.length - 1; i++) {
       const startIdx = segmentIndices[i];
       // if smoothed, the indices don't perfectly map to the new array size.
       // For forceStraight, we just animate the whole line as one anyway, but we need lDists for timing.
       // Let's just push the whole feature at once for the active route!
    }

    // Actually, updateRouteData needs allFeatures. Let's just push it all.
    let legDist = 0;
    for (let j = 0; j < routeFullCoords.length - 1; j++) {
      legDist += distance(routeFullCoords[j], routeFullCoords[j+1]);
    }
    // We can just have one single leg for the whole route, or keep them proportional.
    // If we just use one leg, the animation still works!
    lDists.push(legDist);
    totalPathDist = legDist;

    allFeatures.push({
      type: 'Feature',
      properties: {},
      geometry: { type: 'LineString', coordinates: routeFullCoords }
    });"""

content = content.replace(old_active, new_active)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
