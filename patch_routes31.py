import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Wrap fitBounds in try-catch to prevent crashes
content = re.sub(r'mapRef\.current\.fitBounds\(\[\[minLng, minLat\], \[maxLng, maxLat\]\], \{ padding: 100, duration: 1200 \}\);', r'try { mapRef.current.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200 }); } catch (e) { console.error(e); }', content)
content = re.sub(r'map\.fitBounds\(\[\[minLng, minLat\], \[maxLng, maxLat\]\], \{ padding: 100, duration: 1200 \}\);', r'try { map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200 }); } catch (e) { console.error(e); }', content)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
