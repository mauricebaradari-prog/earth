with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("function updateRouteProgress((", "function updateRouteProgress(")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
