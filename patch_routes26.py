import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

overlay_patch = """      const updateSvgOverlay = () => {
        try {
          if (!mapRef.current) return;
          
          // 1. Calculate FULL path (transparent)
          const fullPts: string[] = [];
          if (fullActiveCoordsRef.current) {
            fullActiveCoordsRef.current.forEach(feat => {
              if (feat.geometry.type === 'LineString') {
                 (feat.geometry.coordinates as [number, number][]).forEach(c => {
                   if (!mapRef.current) return;
                   const p = mapRef.current.project([c[0], c[1]]);
                   if (p && !isNaN(p.x) && !isNaN(p.y)) fullPts.push(`${p.x},${p.y}`);
                 });
              }
            });
          }
          if (fullPts.length > 0) setFullSvgPath(`M ${fullPts.join(' L ')}`);
          else setFullSvgPath('');

          // 2. Calculate sliced path (grown)
          if (routeCoordsRef.current.length === 0) {
            setSvgPath('');
          } else {
            const pts: string[] = [];
            routeCoordsRef.current.forEach(feat => {
              if (feat.geometry.type === 'LineString') {
                 (feat.geometry.coordinates as [number, number][]).forEach(c => {
                   if (!mapRef.current) return;
                   const p = mapRef.current.project([c[0], c[1]]);
                   if (p && !isNaN(p.x) && !isNaN(p.y)) pts.push(`${p.x},${p.y}`);
                 });
              }
            });
            if (pts.length > 0) setSvgPath(`M ${pts.join(' L ')}`);
            else setSvgPath('');
          }
          
          // 3. Calculate INACTIVE paths
          const inacts: {id: string, path: string}[] = [];
          if (inactiveCoordsRef.current) {
            inactiveCoordsRef.current.forEach(ir => {
              const iPts: string[] = [];
              ir.features.forEach(feat => {
                if (feat.geometry.type === 'LineString') {
                   (feat.geometry.coordinates as [number, number][]).forEach(c => {
                     if (!mapRef.current) return;
                     const p = mapRef.current.project([c[0], c[1]]);
                     if (p && !isNaN(p.x) && !isNaN(p.y)) iPts.push(`${p.x},${p.y}`);
                   });
                }
              });
              if (iPts.length > 0) inacts.push({ id: ir.id, path: `M ${iPts.join(' L ')}` });
            });
          }
          setInactivePaths(inacts);

          // 4. Update Distance Badge
          if (midLngLatRef.current && totalDistRef.current > 0) {
            const p = mapRef.current.project(midLngLatRef.current);
            if (p && !isNaN(p.x) && !isNaN(p.y)) {
              // Format video duration
              const h = Math.floor(durationSeconds / 3600);
              const m = Math.floor((durationSeconds % 3600) / 60);
              const s = Math.floor(durationSeconds % 60);
              
              let durationStr = '';
              if (h > 0) durationStr += `${h}h `;
              if (m > 0) durationStr += `${m}m `;
              durationStr += `${s}s`;
              
              setDistanceBadge({ x: p.x, y: p.y, distance: Math.round(totalDistRef.current), duration: durationStr.trim() });
            } else {
              setDistanceBadge(null);
            }
          } else {
            setDistanceBadge(null);
          }

          if (vehicleLngLatRef.current) {
            const p = mapRef.current.project(vehicleLngLatRef.current);
            if (p && !isNaN(p.x) && !isNaN(p.y)) {
              setVehicleDot({ x: p.x, y: p.y });
            } else {
              setVehicleDot(null);
            }
          } else {
            setVehicleDot(null);
          }
        } catch (e) {
          console.error("SVG overlay error", e);
        }
      };"""

content = re.sub(r'      const updateSvgOverlay = \(\) => \{.*?      \};\n      \n      // Store on window so we can call it from updateRouteProgress\n      \(window as any\)\._updateSvgOverlay = updateSvgOverlay;', overlay_patch + '\n      \n      // Store on window so we can call it from updateRouteProgress\n      (window as any)._updateSvgOverlay = updateSvgOverlay;', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
