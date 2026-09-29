const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

const broken = `  // ── Helpers ─────────────────────────────────────────────────────────────────

          type: 'FeatureCollection', 
          features: [
            {
              type: 'Feature',
              properties: {},
              geometry: {
                type: 'LineString',
                coordinates: [
                  [32.4222, 34.7720],
                  [32.4258, 35.0344]
                ]
              }
            }
          ] 
        },
      });
    }
    if (!map.getLayer('route-glow')) {`;

code = code.replace(broken, "  // ── Helpers ─────────────────────────────────────────────────────────────────\n\n    if (!map.getLayer('route-glow')) {");
fs.writeFileSync('src/components/GlobeMap.tsx', code);
