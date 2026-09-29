const fs = require('fs');

// 1. GlobeMap.tsx: Move map controls to bottom-right
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

code = code.replace(
  `map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));`,
  `map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');`
);

// 2. GlobeMap.tsx: Move Elevation profile default y to be below the video
code = code.replace(
  `default={{ x: typeof window !== 'undefined' ? window.innerWidth - 340 : 0, y: 20, width: 320, height: 'auto' }}`,
  `default={{ x: typeof window !== 'undefined' ? window.innerWidth - 340 : 0, y: 300, width: 320, height: 'auto' }}`
);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
