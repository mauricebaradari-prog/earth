import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace('}, [cities]);', '}, [cities, routes, activeRouteId]);')

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
