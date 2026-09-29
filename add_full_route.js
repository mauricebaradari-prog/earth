const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

// 1. Add fullSvgPath state
code = code.replace(
  "const [svgPath, setSvgPath] = React.useState<string>('');",
  "const [svgPath, setSvgPath] = React.useState<string>('');\n  const [fullSvgPath, setFullSvgPath] = React.useState<string>('');"
);

// 2. Update updateSvgOverlay to calculate both
const findUpdateOverlay = `      const updateSvgOverlay = () => {
        if (!mapRef.current || routeCoordsRef.current.length === 0) {
          setSvgPath('');
          return;
        }
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
      };`;

const replaceUpdateOverlay = `      const updateSvgOverlay = () => {
        if (!mapRef.current) return;
        
        // 1. Calculate FULL path
        const fullPts = [];
        for (let i = 0; i < cities.length - 1; i++) {
          const key = \`\${cities[i].id}-\${cities[i+1].id}\`;
          const coords = osrmCacheRef.current[key];
          if (coords) {
             coords.forEach(c => {
               const p = mapRef.current.project([c[0], c[1]]);
               fullPts.push(\`\${p.x},\${p.y}\`);
             });
          }
        }
        if (fullPts.length > 0) setFullSvgPath(\`M \${fullPts.join(' L ')}\`);
        else setFullSvgPath('');

        // 2. Calculate sliced path
        if (routeCoordsRef.current.length === 0) {
          setSvgPath('');
          return;
        }
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
      };`;

code = code.replace(findUpdateOverlay, replaceUpdateOverlay);

// 3. Update JSX to include both paths
const findJSX = `<path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />`;
const replaceJSX = `<path d={fullSvgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeOpacity={0.3} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />`;

code = code.replace(findJSX, replaceJSX);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
