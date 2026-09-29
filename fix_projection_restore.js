const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

code = code.replace(
  `// (map as any).setProjection({ type: 'globe' }); // TEMP DISABLED FOR MOBILE TEST`,
  `(map as any).setProjection({ type: 'globe' });`
);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
