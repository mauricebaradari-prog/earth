# The missing closures are:
# 1. map.once('style.load', () => {
# 2. import('maplibre-gl').then((maplibregl) => {
# 3. useEffect(() => {
import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

patch = """      map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200 });
    }
      });
    });
    
    return () => {
      isMounted = false;
      if (mapInstance) mapInstance.remove();
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── 2. Update Data when cities change ────────────────────────────────────────
  useEffect(() => {
    if (!mapRef.current || !routeInitializedRef.current) return;
    updateRouteData(mapRef.current, ++renderPassRef.current);
    rebuildMarkers(mapRef.current, cities);
    
    const _routes = routes && routes.length > 0 ? routes : ROUTES;
    const allCities = _routes.flatMap(r => r.cities);
    
    if (allCities.length >= 2) {
      const lats = allCities.map((c) => c.lat);
      const lngs = allCities.map((c) => c.lng);
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLng = Math.min(...lngs);
      const maxLng = Math.max(...lngs);
      mapRef.current.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200 });
    }"""

content = re.sub(r'      map\.fitBounds\(\[\[minLng, minLat\], \[maxLng, maxLat\]\], \{ padding: 100, duration: 1200 \}\);\n    \}', patch, content, count=1)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
