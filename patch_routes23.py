import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

fitbounds_patch = """    const _routes = routes && routes.length > 0 ? routes : ROUTES;
    const allCities = _routes.flatMap(r => r.cities);
    
    if (allCities.length >= 2) {
      const lats = allCities.map((c) => c.lat);
      const lngs = allCities.map((c) => c.lng);
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLng = Math.min(...lngs);
      const maxLng = Math.max(...lngs);
      map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200 });
    }"""

content = re.sub(r'    if \(cities\.length >= 2\) \{.*?      map\.fitBounds\(\[\[minLng, minLat\], \[maxLng, maxLat\]\], \{ padding: 100, duration: 1200 \}\);\n    \}', fitbounds_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
