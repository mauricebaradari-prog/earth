import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("  cities: City[];\n  mapStyle: string;", "  cities: City[];\n  routes?: { id: string; name: string; cities: City[] }[];\n  mapStyle: string;")
content = content.replace("  cities,\n  mapStyle,", "  cities,\n  routes,\n  mapStyle,")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
