import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("  cities: City[];", "  cities: City[];\n  routes?: { id: string; name: string; cities: City[] }[];")
content = content.replace("  cities,", "  cities,\n  routes,")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
