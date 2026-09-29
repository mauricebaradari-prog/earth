import json

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

if 'const _routes = routes || [];' in content:
    print("ROUTES PATCH IS PRESENT")
else:
    print("ROUTES PATCH IS MISSING")
