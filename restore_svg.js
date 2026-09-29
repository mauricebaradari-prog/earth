const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

// 1. Re-add SVG state
code = code.replace(
  "const renderPassRef = useRef<number>(0);",
  "const renderPassRef = useRef<number>(0);\n  const [svgPath, setSvgPath] = React.useState<string>('');"
);

// 2. Re-add map.on('render')
const styleLoadFind = `    map.once('style.load', () => {`;
const styleLoadReplace = `      map.on('render', () => {
        if (!mapRef.current || routeCoordsRef.current.length === 0) return;
        const pts = [];
        routeCoordsRef.current.forEach(f => {
          if (f.geometry.type === 'LineString') {
            f.geometry.coordinates.forEach(c => {
              const p = mapRef.current.project([c[0], c[1]]);
              pts.push(\`\${p.x},\${p.y}\`);
            });
          }
        });
        if (pts.length > 0) {
          setSvgPath(\`M \${pts.join(' L ')}\`);
        } else {
          setSvgPath('');
        }
      });\n\n    map.once('style.load', () => {`;
code = code.replace(styleLoadFind, styleLoadReplace);

// 3. Remove MapLibre WebGL layers to prevent duplicate/broken rendering
const layersFind = `        layers: [
          ...baseStyle.layers,
          {
            id: 'route-glow',
            type: 'line',
            source: 'route',
            layout: { 'line-join': 'round', 'line-cap': 'round' },
            paint: { 'line-color': routeColor, 'line-width': routeWidth * 1.5, 'line-opacity': 0.4 }
          },
          {
            id: 'route-line',
            type: 'line',
            source: 'route',
            layout: { 'line-join': 'round', 'line-cap': 'round' },
            paint: { 'line-color': routeColor, 'line-width': routeWidth }
          }
        ]`;
const layersReplace = `        layers: [...baseStyle.layers]`;
code = code.replace(layersFind, layersReplace);

// 4. Re-add SVG to JSX
const jsxFind = `    <div className="absolute inset-0 bg-[#04071200]">
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
    </div>`;
const jsxReplace = `    <div className="absolute inset-0 bg-[#04071200]">
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
      <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth} strokeLinecap="round" strokeLinejoin="round" style={{ filter: \`drop-shadow(0 0 6px \${routeColor}66)\` }} />
      </svg>
    </div>`;
code = code.replace(jsxFind, jsxReplace);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
