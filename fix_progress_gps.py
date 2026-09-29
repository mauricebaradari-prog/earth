import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("updateRouteProgress(map, cities, animationProgress, totalPathDist, lDists);", "updateRouteProgress(map, useGpsTrace && cities.length > 0 ? [cities[0], cities[cities.length-1]] : cities, animationProgress, totalPathDist, lDists);")
content = content.replace("updateRouteProgress(map, cities, animationProgress, totalDistRef.current, legDistancesRef.current);", "updateRouteProgress(map, useGpsTrace && cities.length > 0 ? [cities[0], cities[cities.length-1]] : cities, animationProgress, totalDistRef.current, legDistancesRef.current);")

# We also need to cache the gps trace as the first leg in osrmCacheRef so updateRouteProgress can find it!
# It looks for: osrmCacheRef.current[`${cs[i].id}-${cs[i+1].id}`]
# If we pass [cities[0], cities[cities.length-1]], the key will be `${cities[0].id}-${cities[cities.length-1].id}`
# Let's add that to updateRouteData!

add_cache = """               allFeatures.push({
                 type: 'Feature',
                 properties: {},
                 geometry: { type: 'LineString', coordinates: coords }
               });
               if (cities.length > 0) {
                 osrmCacheRef.current[`${cities[0].id}-${cities[cities.length-1].id}`] = coords;
               }"""

content = content.replace("""               allFeatures.push({
                 type: 'Feature',
                 properties: {},
                 geometry: { type: 'LineString', coordinates: coords }
               });""", add_cache)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
