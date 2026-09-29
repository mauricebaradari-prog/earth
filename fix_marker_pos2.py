import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace again for true midpoint
old_logic = """      if (!route.cities || route.cities.length === 0) return;
      // Place marker exactly in the middle of the route
      const middleIndex = Math.floor(route.cities.length / 2);
      const startCity = route.cities[middleIndex];"""

new_logic = """      if (!route.cities || route.cities.length === 0) return;
      // Place marker exactly in the middle between start and end
      const firstCity = route.cities[0];
      const lastCity = route.cities[route.cities.length - 1];
      const midLng = (firstCity.lng + lastCity.lng) / 2;
      const midLat = (firstCity.lat + lastCity.lat) / 2;"""

content = content.replace(old_logic, new_logic)

# Replace the setLngLat call
content = content.replace(".setLngLat([startCity.lng, startCity.lat])", ".setLngLat([midLng, midLat])")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
