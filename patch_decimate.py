import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_loop = """          const pts: string[] = [];
          if (mapRef.current) {
            for (let i = 0; i < fullPts.length; i++) {
               const proj = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
               pts.push(`${proj.x},${proj.y}`);
            }
          }"""

new_loop = """          const pts: string[] = [];
          if (mapRef.current) {
            // Decimate for performance (max ~500 points projected per frame)
            const step = Math.max(1, Math.floor(fullPts.length / 500));
            for (let i = 0; i < fullPts.length; i += step) {
               const proj = mapRef.current.project([fullPts[i][0], fullPts[i][1]]);
               pts.push(`${proj.x},${proj.y}`);
            }
            // Ensure we always project the exact last point so the line connects to the vehicle dot
            if (fullPts.length > 0 && (fullPts.length - 1) % step !== 0) {
               const last = fullPts[fullPts.length - 1];
               const proj = mapRef.current.project([last[0], last[1]]);
               pts.push(`${proj.x},${proj.y}`);
            }
          }"""

content = content.replace(old_loop, new_loop)

# Do the same for the full screenPts (which represents the faded background track)
old_screen = """if (screenPts.length > 0 && fullSvgPathRef.current) {"""

new_screen = """          const decimatedScreenPts: string[] = [];
          if (mapRef.current && fullRouteCoordsRef.current) {
            const all = fullRouteCoordsRef.current;
            const step = Math.max(1, Math.floor(all.length / 500));
            for (let i = 0; i < all.length; i += step) {
               const proj = mapRef.current.project([all[i][0], all[i][1]]);
               decimatedScreenPts.push(`${proj.x},${proj.y}`);
            }
            if (all.length > 0 && (all.length - 1) % step !== 0) {
               const last = all[all.length - 1];
               const proj = mapRef.current.project([last[0], last[1]]);
               decimatedScreenPts.push(`${proj.x},${proj.y}`);
            }
          }
          if (decimatedScreenPts.length > 0 && fullSvgPathRef.current) {
            fullSvgPathRef.current.setAttribute('d', `M ${decimatedScreenPts.join(' L ')}`);
          }"""

# Remove the old screenPts calculation entirely since we recalculate it above
old_screenpts_calc = """      const screenPts: string[] = [];
      if (mapRef.current && fullRouteCoordsRef.current) {
        fullRouteCoordsRef.current.forEach(pt => {
           const proj = mapRef.current!.project([pt[0], pt[1]]);
           screenPts.push(`${proj.x},${proj.y}`);
        });
      }"""

content = content.replace(old_screenpts_calc, "")
content = content.replace("if (screenPts.length > 0 && fullSvgPathRef.current) {\n            fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);\n          }", new_screen)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
