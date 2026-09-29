import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Add prop
content = content.replace("  showElevation?: boolean;", "  showElevation?: boolean;\n  useGpsTrace?: boolean;")
content = content.replace("  showElevation = true,", "  showElevation = true,\n  useGpsTrace = false,")

# 2. Modify updateRouteData
update_route_data = """  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route')) return;
    
    let totalPathDist = 0;
    let lDists: number[] = [];
    let allFeatures: GeoJSON.Feature[] = [];

    if (useGpsTrace) {
       try {
         const res = await fetch('/gps_route.json');
         if (res.ok) {
            const points = await res.json();
            if (points && points.length > 1) {
               const coords = points.map((p: any) => [p.lng, p.lat] as [number, number]);
               let legDist = 0;
               for (let j = 0; j < coords.length - 1; j++) {
                 legDist += distance(coords[j], coords[j+1]);
               }
               totalPathDist = legDist;
               lDists = [legDist];
               allFeatures.push({
                 type: 'Feature',
                 properties: {},
                 geometry: { type: 'LineString', coordinates: coords }
               });
               
               // To make updateRouteProgress work seamlessly, we will just cache this one big arc
               // under a fake key that corresponds to the first and last city, or we just override the logic
            }
         }
       } catch(e) {
         console.warn("GPS trace fetch failed", e);
       }
    }

    if (!useGpsTrace || allFeatures.length === 0) {
      for (let i = 0; i < cities.length - 1; i++) {
        let routeCoords = null;
        try {
          if (renderPassRef.current !== passId) return;
          const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
          if (osrmCacheRef.current[cacheKey]) {
             routeCoords = osrmCacheRef.current[cacheKey];
          } else {
             const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`);
             const data = await res.json();
             if (data.routes && data.routes[0]) {
               routeCoords = data.routes[0].geometry.coordinates;
             }
          }
        } catch (e) {
          console.warn("OSRM fetch failed, using fallback");
        }

        const finalCoords = routeCoords || greatCircleArc(cities[i], cities[i + 1], 120);
        osrmCacheRef.current[`${cities[i].id}-${cities[i+1].id}`] = finalCoords;

        let legDist = 0;
        for (let j = 0; j < finalCoords.length - 1; j++) {
          legDist += distance(finalCoords[j], finalCoords[j+1]);
        }
        lDists.push(legDist);
        totalPathDist += legDist;

        allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: finalCoords }
        });
      }
    }"""

content = re.sub(r'  async function updateRouteData\(map: MaplibreMap, passId: number\) \{.*?        \}\n      \}\n    \}', update_route_data, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
