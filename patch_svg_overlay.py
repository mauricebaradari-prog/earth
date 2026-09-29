import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_overlay = """          if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);

          // Project inactive routes to SVG
          const inactiveSegments: string[] = [];
          if (mapRef.current) {
            for (const seg of inactiveCoordsRef.current) {
              const segPts = [];
              for (const p of seg) {
                 const proj = mapRef.current.project([p[0], p[1]]);
                 segPts.push(`${proj.x},${proj.y}`);
              }
              if (segPts.length > 0) inactiveSegments.push(`M ${segPts.join(' L ')}`);
            }
          }
          setInactiveSvgPath(inactiveSegments.join(' '));

          const pts: string[] = [];
          fullPts.forEach(pt => {
             if (mapRef.current) {
                const proj = mapRef.current.project([pt[0], pt[1]]);
                pts.push(`${proj.x},${proj.y}`);
             }
          });
          if (pts.length > 0) {
            setSvgPath(`M ${pts.join(' L ')}`);
          }

          if (currentProgress > 0 && currentProgress < 1 && fullPts.length > 0) {
             const exactIdx = currentProgress * (fullPts.length - 1);
             const pIdx = Math.floor(exactIdx);
             const frac = exactIdx - pIdx;
             if (pIdx < fullPts.length - 1) {
               const p1 = fullPts[pIdx];
               const p2 = fullPts[pIdx + 1];
               const lng = p1[0] + frac * (p2[0] - p1[0]);
               const lat = p1[1] + frac * (p2[1] - p1[1]);
               const p = mapRef.current.project([lng, lat]);
               setVehicleDot({ x: p.x, y: p.y });

               const displaySecs = currentProgress * currentDuration;
               const distKm = (totalDistRef.current * (displaySecs / durationRef.current) / 1000).toFixed(1);
               const m = Math.floor(displaySecs / 60);
               const s = Math.floor(displaySecs % 60);
               setDistanceBadge({
                 x: p.x, y: p.y,
                 text: `${distKm} km`,
                 text2: `${m}:${s.toString().padStart(2, '0')}`
               });
             }
          } else {
             setVehicleDot(null);
             setDistanceBadge(null);
          }"""

new_overlay = """          // Defer state updates to avoid React Maximum update depth exceeded errors
          Promise.resolve().then(() => {
            if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);

            // Project inactive routes to SVG
            const inactiveSegments: string[] = [];
            if (mapRef.current) {
              for (const seg of inactiveCoordsRef.current) {
                const segPts = [];
                for (const p of seg) {
                   const proj = mapRef.current.project([p[0], p[1]]);
                   segPts.push(`${proj.x},${proj.y}`);
                }
                if (segPts.length > 0) inactiveSegments.push(`M ${segPts.join(' L ')}`);
              }
            }
            setInactiveSvgPath(inactiveSegments.join(' '));

            const pts: string[] = [];
            fullPts.forEach(pt => {
               if (mapRef.current) {
                  const proj = mapRef.current.project([pt[0], pt[1]]);
                  pts.push(`${proj.x},${proj.y}`);
               }
            });
            if (pts.length > 0) {
              setSvgPath(`M ${pts.join(' L ')}`);
            }

            if (currentProgress > 0 && currentProgress < 1 && fullPts.length > 0) {
               const exactIdx = currentProgress * (fullPts.length - 1);
               const pIdx = Math.floor(exactIdx);
               const frac = exactIdx - pIdx;
               if (pIdx < fullPts.length - 1) {
                 const p1 = fullPts[pIdx];
                 const p2 = fullPts[pIdx + 1];
                 const lng = p1[0] + frac * (p2[0] - p1[0]);
                 const lat = p1[1] + frac * (p2[1] - p1[1]);
                 const p = mapRef.current.project([lng, lat]);
                 setVehicleDot({ x: p.x, y: p.y });

                 const displaySecs = currentProgress * currentDuration;
                 const distKm = (totalDistRef.current * (displaySecs / durationRef.current) / 1000).toFixed(1);
                 const m = Math.floor(displaySecs / 60);
                 const s = Math.floor(displaySecs % 60);
                 setDistanceBadge({
                   x: p.x, y: p.y,
                   text: `${distKm} km`,
                   text2: `${m}:${s.toString().padStart(2, '0')}`
                 });
               }
            } else {
               setVehicleDot(null);
               setDistanceBadge(null);
            }
          });"""

content = content.replace(old_overlay, new_overlay)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
