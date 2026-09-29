const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

// 1. Change import
code = code.replace(
  `import { Palette, Play, Pause, Gauge, RotateCcw, Video, Map } from 'lucide-react';`,
  `import { Palette, Play, Pause, Gauge, RotateCcw, Video, Map as MapIcon } from 'lucide-react';`
);

// 2. Change JSX tag
code = code.replace(
  `<Map size={18} />`,
  `<MapIcon size={18} />`
);

fs.writeFileSync('src/app/page.tsx', code);
