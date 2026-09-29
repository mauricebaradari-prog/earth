import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

map_err_patch = """      });

      map.on('error', (e) => setGlobalErr(e.error ? e.error.message : JSON.stringify(e)));
      
      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));"""

content = content.replace("      });\n\n      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));", map_err_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
