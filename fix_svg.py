import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Fix 1: fullPts
full_pts_old = """          const screenPts = [];
          for (let i = 0; i < fullPts.length; i += step) {
             const p = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (fullPts.length > 0 && (fullPts.length - 1) % step !== 0) {
             const p = mapRef.current.project([fullPts[fullPts.length - 1][0], fullPts[fullPts.length - 1][1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (fullSvgPathRef.current) {
             if (screenPts.length > 0) {
               fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);
             } else {
               fullSvgPathRef.current.setAttribute('d', '');
             }
          }"""

full_pts_new = """          const screenPts = [];
          let lastP: any = null;
          const pushPt = (p: any, arr: string[]) => {
              if (!lastP) arr.push(`M ${p.x},${p.y}`);
              else if (Math.hypot(p.x - lastP.x, p.y - lastP.y) > window.innerWidth / 2) arr.push(`M ${p.x},${p.y}`);
              else arr.push(`L ${p.x},${p.y}`);
              lastP = p;
          };
          for (let i = 0; i < fullPts.length; i += step) {
             const p = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
             pushPt(p, screenPts);
          }
          if (fullPts.length > 0 && (fullPts.length - 1) % step !== 0) {
             const p = mapRef.current.project([fullPts[fullPts.length - 1][0], fullPts[fullPts.length - 1][1]]);
             pushPt(p, screenPts);
          }
          if (fullSvgPathRef.current) {
             if (screenPts.length > 0) {
               fullSvgPathRef.current.setAttribute('d', screenPts.join(' '));
             } else {
               fullSvgPathRef.current.setAttribute('d', '');
             }
          }"""

content = content.replace(full_pts_old, full_pts_new)


# Fix 2: inactiveSegments
inactive_old = """          const inactiveSegments: string[] = [];
          for (const seg of inactiveRouteCoordsRef.current) {
            const segPts: string[] = [];
            for (const c of seg) {
              if (!mapRef.current) continue;
              const p = mapRef.current.project([c[0], c[1]]);
              segPts.push(`${p.x},${p.y}`);
            }
            if (segPts.length > 0) inactiveSegments.push(`M ${segPts.join(' L ')}`);
          }"""

inactive_new = """          const inactiveSegments: string[] = [];
          for (const seg of inactiveRouteCoordsRef.current) {
            const segPts: string[] = [];
            let lastP: any = null;
            for (const c of seg) {
              if (!mapRef.current) continue;
              const p = mapRef.current.project([c[0], c[1]]);
              if (!lastP) segPts.push(`M ${p.x},${p.y}`);
              else if (Math.hypot(p.x - lastP.x, p.y - lastP.y) > window.innerWidth / 2) segPts.push(`M ${p.x},${p.y}`);
              else segPts.push(`L ${p.x},${p.y}`);
              lastP = p;
            }
            if (segPts.length > 0) inactiveSegments.push(segPts.join(' '));
          }"""

content = content.replace(inactive_old, inactive_new)


# Fix 3: pts (active route)
active_old = """          const pts: string[] = [];
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
          if (svgPathRef.current) {
            if (pts.length > 0) {
              svgPathRef.current.setAttribute('d', `M ${pts.join(' L ')}`);
            } else {
              svgPathRef.current.setAttribute('d', '');
            }
          }"""

active_new = """          const pts: string[] = [];
          let lastActiveP: any = null;
          routeCoordsRef.current.forEach((feat) => {
            if (feat.geometry.type === 'LineString') {
               const coords = feat.geometry.coordinates as [number, number][];
               const rStep = Math.max(1, Math.floor(coords.length / 500));
               for (let i = 0; i < coords.length; i += rStep) {
                 const p = mapRef.current!.project([coords[i][0], coords[i][1]]);
                 if (!lastActiveP) pts.push(`M ${p.x},${p.y}`);
                 else if (Math.hypot(p.x - lastActiveP.x, p.y - lastActiveP.y) > window.innerWidth / 2) pts.push(`M ${p.x},${p.y}`);
                 else pts.push(`L ${p.x},${p.y}`);
                 lastActiveP = p;
               }
               if (coords.length > 0 && (coords.length - 1) % rStep !== 0) {
                 const p = mapRef.current!.project([coords[coords.length - 1][0], coords[coords.length - 1][1]]);
                 if (!lastActiveP) pts.push(`M ${p.x},${p.y}`);
                 else if (Math.hypot(p.x - lastActiveP.x, p.y - lastActiveP.y) > window.innerWidth / 2) pts.push(`M ${p.x},${p.y}`);
                 else pts.push(`L ${p.x},${p.y}`);
                 lastActiveP = p;
               }
            }
          });
          if (svgPathRef.current) {
            if (pts.length > 0) {
              svgPathRef.current.setAttribute('d', pts.join(' '));
            } else {
              svgPathRef.current.setAttribute('d', '');
            }
          }"""

content = content.replace(active_old, active_new)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
