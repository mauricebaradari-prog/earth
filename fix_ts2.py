import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("version: 8,", "version: 8 as 8,")
content = content.replace("type: 'raster',", "type: 'raster' as 'raster',")
content = content.replace("type: 'background',", "type: 'background' as 'background',")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
