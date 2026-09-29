import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_active_check = "const activeRoute = state.routes.find(r => r.id === state.activeRouteId);"
new_active_check = "const activeRoute = routes?.find(r => r.cities.length === cities.length && r.cities.every((c, idx) => c.id === cities[idx].id));"

content = content.replace(old_active_check, new_active_check)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
