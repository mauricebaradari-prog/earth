import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Make rebuildMarkers loop over ALL routes
markers_patch = """  function rebuildMarkers(map: MaplibreMap, cs: City[]) {
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];
    const _routes = routes && routes.length > 0 ? routes : ROUTES;

    import('maplibre-gl').then(({ Marker }) => {
      _routes.forEach((r) => {
        const routeCities = r.cities;
        const isActive = r.id === activeRouteId;
        
        routeCities.forEach((city, i) => {
          if (i !== 0 && i !== routeCities.length - 1) return;
          const label = i === 0 ? 'A' : 'B';
          const el = document.createElement('div');
          
          // Make inactive markers slightly transparent
          el.innerHTML = getCityMarkerHTML(label, city.name, i === 0, i === routeCities.length - 1);
          if (!isActive) {
            el.style.opacity = '0.6';
            el.style.cursor = 'pointer';
            el.onclick = () => {
              if ((window as any).__ON_ROUTE_SELECT) (window as any).__ON_ROUTE_SELECT(r.id);
            };
          }
          
          const marker = new Marker({ element: el, anchor: 'bottom' })
            .setLngLat([city.lng, city.lat])
            .addTo(map);
          markersRef.current.push(marker);
        });
      });
    });
  }"""

content = re.sub(r'  function rebuildMarkers\(map: MaplibreMap, cs: City\[\]\) \{.*?    \}\);\n  \}', markers_patch, content, flags=re.DOTALL)

# Reset inactiveCoordsRef to avoid duplicates
update_data_patch = """  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route') || !map.getSource('route-inactive')) return;
    
    let activeMergedCoords: number[][] = [];
    const inactiveFeatures: GeoJSON.Feature[] = [];
    let activeFeatures: GeoJSON.Feature[] = [];
    const _routes = routes && routes.length > 0 ? routes : ROUTES;
    
    inactiveCoordsRef.current = [];
    fullActiveCoordsRef.current = [];
"""

content = content.replace("""  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route') || !map.getSource('route-inactive')) return;
    
    let activeMergedCoords: number[][] = [];
    const inactiveFeatures: GeoJSON.Feature[] = [];
    let activeFeatures: GeoJSON.Feature[] = [];
    const _routes = routes && routes.length > 0 ? routes : ROUTES;""", update_data_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
