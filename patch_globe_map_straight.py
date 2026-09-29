import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_active_reconstruct = """    // Now reconstruct lDists
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

new_active_reconstruct = """    let legDist = 0;
    for (let j = 0; j < routeFullCoords.length - 1; j++) {
      legDist += distance(routeFullCoords[j], routeFullCoords[j+1]);
    }
    
    if (activeRoute?.forceStraight && cities.length > 0) {
       // Treat as a single segment for progress animation
       const fullKey = `${cities[0].id}-${cities[cities.length-1].id}`;
       osrmCacheRef.current[fullKey] = routeFullCoords;
       lDists.push(legDist);
    } else {
       // Restore original lDists for non-smoothed segmented routes
       for (let i = 0; i < cities.length - 1; i++) {
          const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
          const segCoords = osrmCacheRef.current[cacheKey];
          let d = 0;
          for(let k=0; k<segCoords.length-1; k++) d += distance(segCoords[k], segCoords[k+1]);
          lDists.push(d);
       }
    }
    totalPathDist = legDist;

    allFeatures.push({
      type: 'Feature',
      properties: {},
      geometry: { type: 'LineString', coordinates: routeFullCoords }
    });"""

content = content.replace(old_active_reconstruct, new_active_reconstruct)


# Update the progress call
old_progress_call = """updateRouteProgress(map, useGpsTrace && cities.length > 0 ? [cities[0], cities[cities.length-1]] : cities, animationProgress, totalPathDist, lDists);"""
new_progress_call = """updateRouteProgress(map, (useGpsTrace || activeRoute?.forceStraight) && cities.length > 0 ? [cities[0], cities[cities.length-1]] : cities, animationProgress, totalPathDist, lDists);"""
content = content.replace(old_progress_call, new_progress_call)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
