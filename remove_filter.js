const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

const findStr = `<path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth} strokeLinecap="round" strokeLinejoin="round" style={{ filter: \`drop-shadow(0 0 6px \${routeColor}66)\` }} />`;
const replaceStr = `<path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />`;

code = code.replace(findStr, replaceStr);
fs.writeFileSync('src/components/GlobeMap.tsx', code);
