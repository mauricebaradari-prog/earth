const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

const findAnimUpdate = `      if (vehicleMarkerRef.current) {
        vehicleMarkerRef.current.remove();
        vehicleMarkerRef.current = null;
      }
      updateRouteProgress(mapRef.current, cities, animationProgress, totalDist, legDists);`;

const replaceAnimUpdate = `      if (vehicleMarkerRef.current) {
        vehicleMarkerRef.current.remove();
        vehicleMarkerRef.current = null;
      }
      updateRouteProgress(mapRef.current, cities, animationProgress, totalDist, legDists);
      
      if (mapRef.current) {
        mapRef.current.jumpTo({
          center: [pos.lng, pos.lat],
          bearing: animationProgress * 360,
          zoom: 11.5,
          pitch: 65
        });
      }`;

code = code.replace(findAnimUpdate, replaceAnimUpdate);

const findReset = `    if (!isAnimating && animationProgress === 0) {
      removeVehicleMarker();
      updateRouteData(map, cities, currentPass);
      return;
    }`;

const replaceReset = `    if (!isAnimating && animationProgress === 0) {
      removeVehicleMarker();
      updateRouteData(map, cities, currentPass);
      if (cities.length >= 2) {
        const lats = cities.map((c) => c.lat);
        const lngs = cities.map((c) => c.lng);
        const minLat = Math.min(...lats), maxLat = Math.max(...lats);
        const minLng = Math.min(...lngs), maxLng = Math.max(...lngs);
        map.fitBounds([[minLng, minLat], [maxLng, maxLat]], { padding: 100, duration: 1200, pitch: 60, bearing: 0 });
      }
      return;
    }`;

code = code.replace(findReset, replaceReset);

fs.writeFileSync('src/components/GlobeMap.tsx', code);
