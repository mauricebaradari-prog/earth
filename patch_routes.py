import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Add route-inactive layers
init_route_layers_patch = """
  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    if (!map.getSource('route-inactive')) {
      map.addSource('route-inactive', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
    
    if (!map.getLayer('route-inactive-glow')) {
      map.addLayer({
        id: 'route-inactive-glow',
        type: 'line',
        source: 'route-inactive',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': 12,
          'line-opacity': 0.3,
          'line-color': '#FFFFFF'
        }
      });
    }
    if (!map.getLayer('route-inactive-line')) {
      map.addLayer({
        id: 'route-inactive-line',
        type: 'line',
        source: 'route-inactive',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': width * 1.5 + 1,
          'line-opacity': 0.7,
          'line-color': '#FFFFFF'
        }
      });
    }

    if (!map.getSource('route')) {
      map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] },
        lineMetrics: true
      });
    }
    
    const gradient = [
      'interpolate',
      ['linear'],
      ['line-progress'],
      0, '#FFFFFF',
      1, color
    ];

    if (!map.getLayer('route-glow')) {
      map.addLayer({
        id: 'route-glow',
        type: 'line',
        source: 'route',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': 12,
          'line-opacity': 0.5,
          'line-gradient': gradient as any
        }
      });
    }
    if (!map.getLayer('route-line')) {
      map.addLayer({
        id: 'route-line',
        type: 'line',
        source: 'route',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': width * 1.5 + 1,
          'line-opacity': 1,
          'line-gradient': gradient as any
        }
      });
    }

    if (!(map as any)._routeClickAdded) {
      (map as any)._routeClickAdded = true;
      
      // Inactive route click
      map.on('mouseenter', 'route-inactive-glow', () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'route-inactive-glow', () => { map.getCanvas().style.cursor = ''; });
      map.on('click', 'route-inactive-glow', (e) => {
        const feature = e.features?.[0];
        if (feature && feature.properties?.routeId && window.__ON_ROUTE_SELECT) {
          window.__ON_ROUTE_SELECT(feature.properties.routeId);
        }
      });

      // Active route click
      map.on('mouseenter', 'route-glow', () => { map.getCanvas().style.cursor = 'pointer'; });
      map.on('mouseleave', 'route-glow', () => { map.getCanvas().style.cursor = ''; });
      map.on('click', 'route-glow', (e) => {
        if (!window.__ON_SEEK) return;
        const clickLngLat = e.lngLat;
        let closestFrac = 0;
        let minDist = Infinity;
        let totalPathDist = 0;
        const allSegments: { p1: [number, number]; p2: [number, number]; dist: number }[] = [];
        
        window.__ROUTE_COORDS.forEach((feat: any) => {
          if (feat.geometry.type === 'LineString') {
            const coords = feat.geometry.coordinates;
            for (let j = 0; j < coords.length - 1; j++) {
              const d = haversineDistance({ lng: coords[j][0], lat: coords[j][1] }, { lng: coords[j+1][0], lat: coords[j+1][1] });
              totalPathDist += d;
              allSegments.push({ p1: coords[j], p2: coords[j+1], dist: d });
            }
          }
        });

        let distSoFar = 0;
        for (const seg of allSegments) {
          const mid: [number, number] = [ (seg.p1[0] + seg.p2[0]) / 2, (seg.p1[1] + seg.p2[1]) / 2 ];
          const d1 = haversineDistance(clickLngLat, { lng: seg.p1[0], lat: seg.p1[1] });
          const d2 = haversineDistance(clickLngLat, { lng: seg.p2[0], lat: seg.p2[1] });
          const dm = haversineDistance(clickLngLat, { lng: mid[0], lat: mid[1] });
          
          let segDistToClick = d1;
          let fracOnSeg = 0;
          if (d2 < segDistToClick) { segDistToClick = d2; fracOnSeg = 1; }
          if (dm < segDistToClick) { segDistToClick = dm; fracOnSeg = 0.5; }
          
          if (segDistToClick < minDist) {
            minDist = segDistToClick;
            closestFrac = (distSoFar + (seg.dist * fracOnSeg)) / totalPathDist;
          }
          distSoFar += seg.dist;
        }
        
        if (minDist < 50) { window.__ON_SEEK(closestFrac); }
      });
    }
  }
"""

# Replace initRouteLayers
content = re.sub(r'  function initRouteLayers\(.*?\n  async function updateRouteData', init_route_layers_patch + '\n  async function updateRouteData', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)

