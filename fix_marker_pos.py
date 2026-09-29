import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace the startCity logic
old_logic = """      if (!route.cities || route.cities.length === 0) return;
      const startCity = route.cities[0];"""

new_logic = """      if (!route.cities || route.cities.length === 0) return;
      // Place marker exactly in the middle of the route
      const middleIndex = Math.floor(route.cities.length / 2);
      const startCity = route.cities[middleIndex];"""

content = content.replace(old_logic, new_logic)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
