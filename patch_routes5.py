import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace('updateRouteData(map, cities, renderPassRef.current)', 'updateRouteData(map, renderPassRef.current)')

# Let's also attach window globals in an effect so they are accessible to map.on('click')
effect_patch = """  useEffect(() => {
    (window as any).__ON_SEEK = onSeek;
    (window as any).__ON_ROUTE_SELECT = onRouteSelect;
  }, [onSeek, onRouteSelect]);

  // ── 1. Init map ──────────────────────────────────────────────────────────────"""

content = content.replace('  // ── 1. Init map ──────────────────────────────────────────────────────────────', effect_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
