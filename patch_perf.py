import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Remove state variables
content = re.sub(r'const \[vehicleDot, setVehicleDot\].*?\n', '', content)
content = re.sub(r'const \[distanceBadge, setDistanceBadge\].*?\n', '', content)
content = re.sub(r'const \[fullSvgPath, setFullSvgPath\].*?\n', '', content)
content = re.sub(r'const \[svgPath, setSvgPath\].*?\n', '', content)
content = re.sub(r'const \[inactiveSvgPath, setInactiveSvgPath\].*?\n', '', content)

# 2. Add refs for DOM elements
refs = """  const vehicleDotRef = React.useRef<HTMLDivElement>(null);
  const distanceBadgeRef = React.useRef<HTMLDivElement>(null);
  const distanceTextRef = React.useRef<HTMLSpanElement>(null);
  const distanceTimeRef = React.useRef<HTMLSpanElement>(null);
  const fullSvgPathRef = React.useRef<SVGPathElement>(null);
  const svgPathRef = React.useRef<SVGPathElement>(null);"""

content = content.replace("const osrmCacheRef = React.useRef<Record<string, any>>({});", refs + "\n  const osrmCacheRef = React.useRef<Record<string, any>>({});")

# 3. Update updateSvgOverlay to use DOM mutations directly
old_overlay = """          // Defer state updates to avoid React Maximum update depth exceeded errors
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

new_overlay = """          // Direct DOM Mutation for 60fps performance (bypasses React renders entirely)
          if (screenPts.length > 0 && fullSvgPathRef.current) {
            fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);
          }

          const pts: string[] = [];
          if (mapRef.current) {
            for (let i = 0; i < fullPts.length; i++) {
               const proj = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
               pts.push(`${proj.x},${proj.y}`);
            }
          }
          if (pts.length > 0 && svgPathRef.current) {
            svgPathRef.current.setAttribute('d', `M ${pts.join(' L ')}`);
          }

          if (currentProgress > 0 && currentProgress < 1 && fullPts.length > 0) {
             const exactIdx = currentProgress * (fullPts.length - 1);
             const pIdx = Math.floor(exactIdx);
             const frac = exactIdx - pIdx;
             if (pIdx < fullPts.length - 1 && mapRef.current) {
               const p1 = fullPts[pIdx];
               const p2 = fullPts[pIdx + 1];
               const lng = p1[0] + frac * (p2[0] - p1[0]);
               const lat = p1[1] + frac * (p2[1] - p1[1]);
               const p = mapRef.current.project([lng, lat]);
               
               if (vehicleDotRef.current) {
                 vehicleDotRef.current.style.transform = `translate(${p.x}px, ${p.y}px)`;
                 vehicleDotRef.current.style.display = 'block';
               }

               if (distanceBadgeRef.current && distanceTextRef.current && distanceTimeRef.current) {
                 distanceBadgeRef.current.style.transform = `translate(${p.x}px, ${p.y}px)`;
                 distanceBadgeRef.current.style.display = 'flex';
                 
                 const displaySecs = currentProgress * currentDuration;
                 const distKm = (totalDistRef.current * (displaySecs / durationRef.current) / 1000).toFixed(1);
                 const m = Math.floor(displaySecs / 60);
                 const s = Math.floor(displaySecs % 60);
                 
                 distanceTextRef.current.textContent = `${distKm} km`;
                 distanceTimeRef.current.textContent = `${m}:${s.toString().padStart(2, '0')}`;
               }
             }
          } else {
             if (vehicleDotRef.current) vehicleDotRef.current.style.display = 'none';
             if (distanceBadgeRef.current) distanceBadgeRef.current.style.display = 'none';
          }"""

content = content.replace(old_overlay, new_overlay)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
