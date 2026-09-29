const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

// 1. Hide the vehicle marker completely
const markerUpdateFind = `        if (vehicleMarkerRef.current) {
          vehicleMarkerRef.current.setLngLat([pos.lng, pos.lat]);
          vehicleMarkerRef.current.setRotation(hdg - 45);
          const existingEl = vehicleMarkerRef.current.getElement();
          existingEl.innerHTML = svgStr;
          existingEl.style.filter = \`drop-shadow(0 0 6px \${vehicle.color}88)\`;
        } else {
          const el = document.createElement('div');
          el.innerHTML = svgStr;
          el.style.transformOrigin = 'center';
          el.style.filter = \`drop-shadow(0 0 6px \${vehicle.color}88)\`;
          el.style.transition = 'transform 0.1s ease';
          
          vehicleMarkerRef.current = new Marker({ element: el, anchor: 'center', rotation: hdg - 45 })
            .setLngLat([pos.lng, pos.lat])
            .addTo(mapRef.current);
        }`;

const markerUpdateReplace = `        // User requested no vehicle, just the line animation
        if (vehicleMarkerRef.current) {
          vehicleMarkerRef.current.remove();
          vehicleMarkerRef.current = null;
        }`;

code = code.replace(markerUpdateFind, markerUpdateReplace);
fs.writeFileSync('src/components/GlobeMap.tsx', code);
