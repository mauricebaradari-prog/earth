import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Remove fitBounds completely to prevent WebGL crashes
content = re.sub(r'try \{ mapRef\.current\.fitBounds.*?\} catch \(e\) \{ console\.error\(e\); \}', '', content, flags=re.DOTALL)
content = re.sub(r'try \{ map\.fitBounds.*?\} catch \(e\) \{ console\.error\(e\); \}', '', content, flags=re.DOTALL)
content = re.sub(r'map\.fitBounds\(\[\[minLng, minLat\], \[maxLng, maxLat\]\], \{ padding: 100, duration: 1200 \}\);', '', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
