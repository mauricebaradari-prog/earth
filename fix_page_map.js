const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

// 1. Imports
code = code.replace(
  `import CameraPanel from '@/components/panels/CameraPanel';`,
  `import CameraPanel from '@/components/panels/CameraPanel';\nimport MapPanel from '@/components/panels/MapPanel';`
);

code = code.replace(
  `import { Palette, Play, Pause, Gauge, RotateCcw, Video } from 'lucide-react';`,
  `import { Palette, Play, Pause, Gauge, RotateCcw, Video, Map } from 'lucide-react';`
);

// 2. State type
code = code.replace(
  `useState<'none' | 'style' | 'speed' | 'camera'>('none')`,
  `useState<'none' | 'map' | 'style' | 'speed' | 'camera'>('none')`
);

// 3. New Map Button (insert before Palette)
const findPaletteButton = `            <button
              onClick={() => setOpenModal(openModal === 'style' ? 'none' : 'style')}
              className={\`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border \${
                openModal === 'style' 
                  ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }\`}
              title="Map Style"
            >
              <Palette size={18} />
            </button>`;

const newMapButton = `
            <button
              onClick={() => setOpenModal(openModal === 'map' ? 'none' : 'map')}
              className={\`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border \${
                openModal === 'map' 
                  ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }\`}
              title="Map Style"
            >
              <Map size={18} />
            </button>`;
// Change the Palette title to "Route Style"
const modifiedPaletteButton = findPaletteButton.replace('title="Map Style"', 'title="Route Style"');

code = code.replace(findPaletteButton, newMapButton + '\n' + modifiedPaletteButton);

// 4. Panel offset math
const findTopMath = `top: openModal === 'style' ? 48 : openModal === 'speed' ? 96 : openModal === 'camera' ? 144 : 0`;
const replaceTopMath = `top: openModal === 'map' ? 48 : openModal === 'style' ? 96 : openModal === 'speed' ? 144 : openModal === 'camera' ? 192 : 0`;
code = code.replace(findTopMath, replaceTopMath);

// 5. Add MapPanel
const findFloatingEnd = `              {openModal === 'style' && (`;
const newMapModal = `              {openModal === 'map' && (
                <MapPanel
                  mapStyle={state.mapStyle}
                  onMapStyle={setMapStyle}
                />
              )}\n`;
code = code.replace(findFloatingEnd, newMapModal + findFloatingEnd);

fs.writeFileSync('src/app/page.tsx', code);
