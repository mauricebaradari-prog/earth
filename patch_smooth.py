import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Add Chaikin smoothing algorithm at the top of the file
smooth_func = """
// Smooths a polyline using Chaikin's algorithm
function smoothCoords(coords: [number, number][], iterations = 2): [number, number][] {
  if (coords.length < 3) return coords;
  let current = [...coords];
  for (let iter = 0; iter < iterations; iter++) {
    const next: [number, number][] = [];
    next.push(current[0]);
    for (let i = 0; i < current.length - 1; i++) {
      const p0 = current[i];
      const p1 = current[i + 1];
      const q = [0.75 * p0[0] + 0.25 * p1[0], 0.75 * p0[1] + 0.25 * p1[1]] as [number, number];
      const r = [0.25 * p0[0] + 0.75 * p1[0], 0.25 * p0[1] + 0.75 * p1[1]] as [number, number];
      next.push(q);
      next.push(r);
    }
    next.push(current[current.length - 1]);
    current = next;
  }
  return current;
}
"""

if "function smoothCoords" not in content:
    content = content.replace("export default function GlobeMap", smooth_func + "\nexport default function GlobeMap")

# 1. Update Inactive routes to smooth when forceStraight is true
old_inactive = """        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        const coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        allCoordSegments.push(coords);"""

new_inactive = """        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        const coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        const finalCoords = route.forceStraight ? smoothCoords(coords, 3) : coords;
        allCoordSegments.push(finalCoords);"""

content = content.replace(old_inactive, new_inactive)

# 2. Update Active route to smooth when forceStraight is true
old_active = """      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      const finalCoords = osrmCacheRef.current[cacheKey] || greatCircleArc(cities[i], cities[i + 1], 120);
      osrmCacheRef.current[cacheKey] = finalCoords;"""

new_active = """      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      let finalCoords = osrmCacheRef.current[cacheKey] || greatCircleArc(cities[i], cities[i + 1], 120);
      if (activeRoute?.forceStraight) {
        finalCoords = smoothCoords(finalCoords, 3);
      }
      osrmCacheRef.current[cacheKey] = finalCoords;"""

content = content.replace(old_active, new_active)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
