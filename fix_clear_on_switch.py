import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_code = """  // \u2500\u2500 3. Cities update \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    renderPassRef.current += 1;
    legDistancesRef.current = [];
    updateRouteData(map, renderPassRef.current);"""

new_code = """  // \u2500\u2500 3. Cities update \u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    renderPassRef.current += 1;
    legDistancesRef.current = [];
    
    // Clear old SVG traces immediately when switching routes
    routeCoordsRef.current = [];
    fullRouteCoordsRef.current = [];
    if (svgPathRef.current) svgPathRef.current.setAttribute('d', '');
    if (fullSvgPathRef.current) fullSvgPathRef.current.setAttribute('d', '');
    
    updateRouteData(map, renderPassRef.current);"""

content = content.replace(old_code, new_code)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
