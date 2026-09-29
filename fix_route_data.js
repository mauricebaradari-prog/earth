const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

// 1. Clear legDistancesRef in the cities useEffect
code = code.replace(
  `    renderPassRef.current += 1;\n    updateRouteData(map, renderPassRef.current);\n    rebuildMarkers(map, cities);`,
  `    renderPassRef.current += 1;\n    legDistancesRef.current = [];\n    updateRouteData(map, renderPassRef.current);\n    rebuildMarkers(map, cities);`
);

// 2. Call updateRouteProgress at the end of updateRouteData
code = code.replace(
  `    if (map.getSource('route')) {\n      (map.getSource('route') as GeoJSONSource).setData({\n        type: 'FeatureCollection',\n        features: allFeatures,\n      });\n    }`,
  `    if (map.getSource('route')) {\n      (map.getSource('route') as GeoJSONSource).setData({\n        type: 'FeatureCollection',\n        features: allFeatures,\n      });\n    }\n    \n    updateRouteProgress(map, cities, animProgressRef.current, totalPathDist, lDists);\n    if ((window as any)._updateSvgOverlay) {\n      (window as any)._updateSvgOverlay();\n    }`
);

// 3. Add protection to updateRouteProgress
code = code.replace(
  `  function updateRouteProgress(\n    map: MaplibreMap,\n    cs: City[],\n    progress: number,\n    totalDist: number,\n    legDists: number[]\n  ) {\n    \n    if (!map.getSource('route')) return;`,
  `  function updateRouteProgress(\n    map: MaplibreMap,\n    cs: City[],\n    progress: number,\n    totalDist: number,\n    legDists: number[]\n  ) {\n    \n    if (!map.getSource('route') || legDists.length !== cs.length - 1) return;`
);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
