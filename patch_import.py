import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()
content = content.replace("import maplibregl, { Map as MaplibreMap, GeoJSONSource } from 'maplibre-gl';", "import * as maplibregl from 'maplibre-gl';\ntype MaplibreMap = maplibregl.Map;\ntype GeoJSONSource = maplibregl.GeoJSONSource;")
with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
