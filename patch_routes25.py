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

          if (vehicleLngLatRef.current) {
            const p = mapRef.current.project(vehicleLngLatRef.current);
            setVehicleDot({ x: p.x, y: p.y });
          }
        } catch(e) {}
      };"""

content = re.sub(r'      const updateSvgOverlay = \(\) => \{.*?      \};\n\s*\(window as any\)\._updateSvgOverlay = updateSvgOverlay;', overlay_patch + '\n      (window as any)._updateSvgOverlay = updateSvgOverlay;', content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
