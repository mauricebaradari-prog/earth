const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

// Add import
const importMap = `import GlobeMap from '../components/GlobeMap';`;
code = code.replace(importMap, `import GlobeMap from '../components/GlobeMap';\nimport YouTubeOverlay from '../components/YouTubeOverlay';`);

// Add component
const findMapArea = `      {/* Map area */}
      <div className="flex-1 relative bg-[#040712]">
        <GlobeMap`;
const replaceMapArea = `      {/* Map area */}
      <div className="flex-1 relative bg-[#040712]">
        <YouTubeOverlay />
        <GlobeMap`;
code = code.replace(findMapArea, replaceMapArea);

fs.writeFileSync('src/app/page.tsx', code);
