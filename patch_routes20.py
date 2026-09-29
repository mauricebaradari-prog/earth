import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Restore the slicing logic in updateRouteProgress so svgPath grows
progress_patch = """  function updateRouteProgress(
    map: MaplibreMap,
    cs: City[],
    progress: number,
    totalDist: number,
    legDists: number[]
  ) {
    if (!map.getSource('route')) return;

    let remaining = progress;
    let vehiclePoint = cs[0] ? [cs[0].lng, cs[0].lat] : [0,0];
    const newActiveFeatures: GeoJSON.Feature[] = [];

    for (let i = 0; i < cs.length - 1; i++) {
      const legFrac = legDists[i] / totalDist;
      const legProgress = Math.min(1, remaining / legFrac);
      remaining -= legFrac;

      const fullArc = osrmCacheRef.current[`${cs[i].id}-${cs[i+1].id}`] || greatCircleArc(cs[i], cs[i + 1], 120);
      const exactIdx = legProgress * (fullArc.length - 1);
      const numCompletePoints = Math.floor(exactIdx) + 1;
      
      const partialArc = fullArc.slice(0, numCompletePoints);
      
      if (legProgress > 0 && legProgress < 1 && numCompletePoints < fullArc.length) {
         const p1 = fullArc[numCompletePoints - 1];
         const p2 = fullArc[numCompletePoints];
         const frac = exactIdx - (numCompletePoints - 1);
         vehiclePoint = [
           p1[0] + (p2[0] - p1[0]) * frac,
           p1[1] + (p2[1] - p1[1]) * frac
         ];
         partialArc.push(vehiclePoint as [number, number]);
      } else if (legProgress === 1) {
         vehiclePoint = fullArc[fullArc.length - 1];
      }

      if (partialArc.length > 1) {
         newActiveFeatures.push({
           type: 'Feature',
           properties: {},
           geometry: { type: 'LineString', coordinates: partialArc }
         });
      }

      if (remaining <= 0) break;
    }

    vehicleLngLatRef.current = vehiclePoint as [number, number];
    routeCoordsRef.current = newActiveFeatures;

    if ((window as any)._updateSvgOverlay) {
      (window as any)._updateSvgOverlay();
    }
  }"""

content = re.sub(r'  function updateRouteProgress\([^)]+\) \{.*?    \}\n  \}', progress_patch, content, flags=re.DOTALL)


# 2. Rewrite the SVG overlay and state to support inactive paths and gradients
svg_state_patch = """  const [fullSvgPath, setFullSvgPath] = React.useState('');
  const [svgPath, setSvgPath] = React.useState('');
  const [inactivePaths, setInactivePaths] = React.useState<{id: string, path: string}[]>([]);
  const [vehicleDot, setVehicleDot] = React.useState<{x:number,y:number}|null>(null);
  
  // We need the full active coords for fullSvgPath
  const fullActiveCoordsRef = useRef<GeoJSON.Feature[]>([]);
  const inactiveCoordsRef = useRef<{id: string, features: GeoJSON.Feature[]}[]>([]);
"""
content = re.sub(r'  const \[fullSvgPath, setFullSvgPath\] = React\.useState\(''\);\n  const \[svgPath, setSvgPath\] = React\.useState\(''\);\n  const \[vehicleDot, setVehicleDot\] = React\.useState<\{x:number,y:number\}\|null>\(null\);', svg_state_patch, content)


# 3. Store full active coords and inactive coords in updateRouteData
update_data_patch = """      if (r.id === activeRouteId) {
        activeFeatures = rFeatures;
        fullActiveCoordsRef.current = rFeatures;
      } else {
        inactiveFeatures.push(...rFeatures);
        inactiveCoordsRef.current.push({ id: r.id, features: rFeatures });
      }
    }
    
    // reset current partial features to full
    routeCoordsRef.current = activeFeatures;
"""
content = re.sub(r'      if \(r\.id === activeRouteId\) \{.*?      \} else \{\n        inactiveFeatures\.push\(\.\.\.rFeatures\);\n      \}\n    \}', update_data_patch, content, flags=re.DOTALL)
content = content.replace("    routeCoordsRef.current = activeFeatures;", "") # removed from below


# 4. Update the updateSvgOverlay function to draw inactive routes and the full active route
overlay_patch = """    const updateSvgOverlay = () => {
      if (!mapRef.current) return;
      
      // Active route partial
      if (routeCoordsRef.current.length > 0) {
        let pts: [number, number][] = [];
        routeCoordsRef.current.forEach((feat) => {
          if (feat.geometry.type === 'LineString') {
            pts = pts.concat(feat.geometry.coordinates as [number, number][]);
          }
        });
        const screenPts = [];
        for (const c of pts) {
          const p = mapRef.current.project([c[0], c[1]]);
          screenPts.push(`${p.x},${p.y}`);
        }
        if (screenPts.length > 0) setSvgPath(`M ${screenPts.join(' L ')}`);
      }
      
      // Active route full
      if (fullActiveCoordsRef.current.length > 0) {
        let pts: [number, number][] = [];
        fullActiveCoordsRef.current.forEach((feat) => {
          if (feat.geometry.type === 'LineString') {
            pts = pts.concat(feat.geometry.coordinates as [number, number][]);
          }
        });
        const screenPts = [];
        for (const c of pts) {
          const p = mapRef.current.project([c[0], c[1]]);
          screenPts.push(`${p.x},${p.y}`);
        }
        if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);
      }
      
      // Inactive routes
      const inacts: {id: string, path: string}[] = [];
      for (const ir of inactiveCoordsRef.current) {
        let pts: [number, number][] = [];
        ir.features.forEach((feat) => {
          if (feat.geometry.type === 'LineString') {
            pts = pts.concat(feat.geometry.coordinates as [number, number][]);
          }
        });
        const screenPts = [];
        for (const c of pts) {
          const p = mapRef.current.project([c[0], c[1]]);
          screenPts.push(`${p.x},${p.y}`);
        }
        if (screenPts.length > 0) inacts.push({ id: ir.id, path: `M ${screenPts.join(' L ')}` });
      }
      setInactivePaths(inacts);
      
      if (vehicleLngLatRef.current) {
        const p = mapRef.current.project(vehicleLngLatRef.current);
        setVehicleDot({ x: p.x, y: p.y });
      }
    };"""

content = re.sub(r'    const updateSvgOverlay = \(\) => \{.*?    \};\n    \(window as any\)\._updateSvgOverlay = updateSvgOverlay;', overlay_patch + '\n    (window as any)._updateSvgOverlay = updateSvgOverlay;', content, flags=re.DOTALL)


# 5. Restore the SVG in JSX and add linearGradient
jsx_patch = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor={routeColor} />
          </linearGradient>
        </defs>
        
        {/* Inactive Routes (clickable) */}
        {inactivePaths.map((ip) => (
          <path 
            key={ip.id}
            d={ip.path} 
            fill="none" 
            stroke="#FFFFFF" 
            strokeWidth={routeWidth * 1.5 + 2} 
            strokeOpacity={0.4} 
            strokeLinecap="round" 
            strokeLinejoin="round"
            style={{ pointerEvents: 'auto', cursor: 'pointer' }}
            onClick={() => onRouteSelect && onRouteSelect(ip.id)}
          />
        ))}

        {/* Active Route Full (transparent) */}
        <path d={fullSvgPath} fill="none" stroke="url(#routeGradient)" strokeWidth={routeWidth * 1.5 + 2} strokeOpacity={0.3} strokeLinecap="round" strokeLinejoin="round" />
        
        {/* Active Route Grown */}
        <path d={svgPath} fill="none" stroke="url(#routeGradient)" strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
      </svg>"""

content = re.sub(r"      <svg xmlns=\"http://www\.w3\.org/2000/svg\" style=\{\{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 \}\}>.*?</svg>", jsx_patch, content, flags=re.DOTALL)


with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
