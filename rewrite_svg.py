import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_func = """      const updateSvgOverlay = () => {
        try {
          if (!mapRef.current) return;
          
          let fullPts = fullRouteCoordsRef.current;


          const currentProgress = animProgressRef.current;
          const currentDuration = durationRef.current;
          if (currentProgress === 0 && fullPts.length > 0 && onPoint1Projected) {
             const p1 = mapRef.current.project([fullPts[0][0], fullPts[0][1]]);
             // Only call if it moved significantly to avoid spam
             if (!(window as any)._lastP1 || Math.abs((window as any)._lastP1.x - p1.x) > 10 || Math.abs((window as any)._lastP1.y - p1.y) > 10) {
               (window as any)._lastP1 = { x: p1.x, y: p1.y };
               Promise.resolve().then(() => onPoint1Projected(p1.x, p1.y));
             }
          }
          const screenPts = [];
          for (const c of fullPts) {
             if (!mapRef.current) continue;
                 const p = mapRef.current.project([c[0], c[1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);

          // Project inactive routes to SVG
          const inactiveSegments: string[] = [];
          for (const seg of inactiveRouteCoordsRef.current) {
            const segPts: string[] = [];
            for (const c of seg) {
              if (!mapRef.current) continue;
              const p = mapRef.current.project([c[0], c[1]]);
              segPts.push(`${p.x},${p.y}`);
            }
            if (segPts.length > 0) inactiveSegments.push(`M ${segPts.join(' L ')}`);
          }
          setInactiveSvgPath(inactiveSegments.join(' '));

          const pts: string[] = [];
          routeCoordsRef.current.forEach((feat) => {
            if (feat.geometry.type === 'LineString') {
               const coords = feat.geometry.coordinates as [number, number][];
               for (const c of coords) {
                 if (!mapRef.current) continue;
                 const p = mapRef.current.project([c[0], c[1]]);
                 pts.push(`${p.x},${p.y}`);
               }
            }
          });
          if (pts.length > 0) {
            setSvgPath(`M ${pts.join(' L ')}`);
          }

          if (vehicleLngLatRef.current) {
             const p = mapRef.current.project(vehicleLngLatRef.current);
             setVehicleDot({ x: p.x, y: p.y });
             
             const currentProgress = animProgressRef.current;
             const currentDuration = durationRef.current;
             
             let displayDist = totalDistRef.current / 1000;
             let displaySecs = currentDuration;
             
             if (currentProgress > 0) {
               displayDist = displayDist * currentProgress;
               displaySecs = currentDuration * (1 - currentProgress);
             }
             
             const distKm = displayDist.toFixed(0);
             const m = Math.floor(displaySecs / 60);
             const s = Math.floor(displaySecs % 60);
             setDistanceBadge({
               x: p.x, y: p.y,
               text: `${distKm} km`,
               text2: `${m}m ${s}s`
             });
          }
        } catch (e) {
           console.error(e);
        }
      };"""

new_func = """      const updateSvgOverlay = () => {
        try {
          if (!mapRef.current) return;
          
          let fullPts = fullRouteCoordsRef.current;
          const currentProgress = animProgressRef.current;
          const currentDuration = durationRef.current;
          
          if (currentProgress === 0 && fullPts.length > 0 && onPoint1Projected) {
             const p1 = mapRef.current.project([fullPts[0][0], fullPts[0][1]]);
             if (!(window as any)._lastP1 || Math.abs((window as any)._lastP1.x - p1.x) > 10 || Math.abs((window as any)._lastP1.y - p1.y) > 10) {
               (window as any)._lastP1 = { x: p1.x, y: p1.y };
               Promise.resolve().then(() => onPoint1Projected(p1.x, p1.y));
             }
          }
          
          // Decimate for performance
          const step = Math.max(1, Math.floor(fullPts.length / 500));
          const screenPts = [];
          for (let i = 0; i < fullPts.length; i += step) {
             const p = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (fullPts.length > 0 && (fullPts.length - 1) % step !== 0) {
             const p = mapRef.current.project([fullPts[fullPts.length - 1][0], fullPts[fullPts.length - 1][1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (screenPts.length > 0 && fullSvgPathRef.current) {
             fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);
          }

          const pts: string[] = [];
          routeCoordsRef.current.forEach((feat) => {
            if (feat.geometry.type === 'LineString') {
               const coords = feat.geometry.coordinates as [number, number][];
               const rStep = Math.max(1, Math.floor(coords.length / 500));
               for (let i = 0; i < coords.length; i += rStep) {
                 const p = mapRef.current!.project([coords[i][0], coords[i][1]]);
                 pts.push(`${p.x},${p.y}`);
               }
               if (coords.length > 0 && (coords.length - 1) % rStep !== 0) {
                 const p = mapRef.current!.project([coords[coords.length - 1][0], coords[coords.length - 1][1]]);
                 pts.push(`${p.x},${p.y}`);
               }
            }
          });
          if (pts.length > 0 && svgPathRef.current) {
            svgPathRef.current.setAttribute('d', `M ${pts.join(' L ')}`);
          }

          if (vehicleLngLatRef.current) {
             const p = mapRef.current.project(vehicleLngLatRef.current);
             
             if (vehicleDotRef.current) {
                 vehicleDotRef.current.style.transform = `translate(${p.x}px, ${p.y}px)`;
                 vehicleDotRef.current.style.display = 'block';
             }
             
             let displayDist = totalDistRef.current / 1000;
             let displaySecs = currentDuration;
             
             if (currentProgress > 0) {
               displayDist = displayDist * currentProgress;
               displaySecs = currentDuration * (1 - currentProgress);
             }
             
             const distKm = displayDist.toFixed(0);
             const m = Math.floor(displaySecs / 60);
             const s = Math.floor(displaySecs % 60);
             
             if (distanceBadgeRef.current && distanceTextRef.current && distanceTimeRef.current) {
                 distanceBadgeRef.current.style.transform = `translate(${p.x}px, ${p.y}px)`;
                 distanceBadgeRef.current.style.display = 'flex';
                 distanceTextRef.current.textContent = `${distKm} km`;
                 distanceTimeRef.current.textContent = `${m}m ${s}s`;
             }
          } else {
             if (vehicleDotRef.current) vehicleDotRef.current.style.display = 'none';
             if (distanceBadgeRef.current) distanceBadgeRef.current.style.display = 'none';
          }
        } catch (e) {
           console.error(e);
        }
      };"""

content = content.replace(old_func, new_func)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
