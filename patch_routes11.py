import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# First, restore updateRouteProgress to just update vehicle and gradient
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

    for (let i = 0; i < cs.length - 1; i++) {
      const legFrac = legDists[i] / totalDist;
      const legProgress = Math.min(1, remaining / legFrac);
      remaining -= legFrac;

      const fullArc = osrmCacheRef.current[`${cs[i].id}-${cs[i+1].id}`] || greatCircleArc(cs[i], cs[i + 1], 120);
      const exactIdx = legProgress * (fullArc.length - 1);
      const numCompletePoints = Math.floor(exactIdx) + 1;
      
      if (legProgress > 0 && legProgress < 1 && numCompletePoints < fullArc.length) {
         const p1 = fullArc[numCompletePoints - 1];
         const p2 = fullArc[numCompletePoints];
         const frac = exactIdx - (numCompletePoints - 1);
         vehiclePoint = [
           p1[0] + (p2[0] - p1[0]) * frac,
           p1[1] + (p2[1] - p1[1]) * frac
         ];
      } else if (legProgress === 1) {
         vehiclePoint = fullArc[fullArc.length - 1];
      }

      if (remaining <= 0) break;
    }

    vehicleLngLatRef.current = vehiclePoint as [number, number];

    // Update gradient so the line grows
    const safeProgress = Math.max(0.001, Math.min(progress, 1));
    const gradient = [
      'interpolate',
      ['linear'],
      ['line-progress'],
      0, '#FFFFFF',
      safeProgress, routeColor,
      safeProgress + 0.00001, 'rgba(255,255,255,0)',
      1, 'rgba(255,255,255,0)'
    ];

    if (map.getLayer('route-glow')) {
      map.setPaintProperty('route-glow', 'line-gradient', gradient);
    }
    if (map.getLayer('route-line')) {
      map.setPaintProperty('route-line', 'line-gradient', gradient);
    }

    if ((window as any)._updateSvgOverlay) {"""

match = re.search(r'  function updateRouteProgress\([^)]+\) \{.*?if \(\(window as any\)\._updateSvgOverlay\) \{', content, re.DOTALL)
if match:
    content = content[:match.start()] + progress_patch + content[match.end() - len('if ((window as any)._updateSvgOverlay) {'):]

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
