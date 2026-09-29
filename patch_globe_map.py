import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace active route fetch
old_active = """      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      if (!osrmCacheRef.current[cacheKey]) {
        const p = fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`)"""

new_active = """      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      const activeRoute = state.routes.find(r => r.id === state.activeRouteId);
      if (!osrmCacheRef.current[cacheKey] && !activeRoute?.forceStraight) {
        const p = fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`)"""

content = content.replace(old_active, new_active)

# Replace inactive route fetch
old_inactive = """        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        if (!osrmCacheRef.current[cacheKey]) {
          const p = fetch(`https://router.project-osrm.org/route/v1/driving/${route.cities[i].lng},${route.cities[i].lat};${route.cities[i+1].lng},${route.cities[i+1].lat}?geometries=geojson`)"""

new_inactive = """        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        if (!osrmCacheRef.current[cacheKey] && !route.forceStraight) {
          const p = fetch(`https://router.project-osrm.org/route/v1/driving/${route.cities[i].lng},${route.cities[i].lat};${route.cities[i+1].lng},${route.cities[i+1].lat}?geometries=geojson`)"""

content = content.replace(old_inactive, new_inactive)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
