import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

elev_patch = """    // Fetch elevation profile
    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      const sampledPts = [];
      const numSamples = 60;
      for (let i = 0; i < numSamples; i++) {
        const idx = Math.floor((i / (numSamples - 1)) * (allCoords.length - 1));
        sampledPts.push(allCoords[idx]);
      }
      const lats = sampledPts.map(p => p[1].toFixed(5)).join(',');
      const lngs = sampledPts.map(p => p[0].toFixed(5)).join(',');
      fetch(`https://api.open-meteo.com/v1/elevation?latitude=${lats}&longitude=${lngs}`)
        .then(r => r.json())
        .then(d => {
          if (d.elevation) setElevationProfile(d.elevation);
        })
        .catch(e => console.error("Elevation fetch failed", e));
    }

    updateRouteProgress(map, cities, animationProgress, totalPathDist, lDists);
"""

content = content.replace("""    // Simulate elevation profile
    const fakeElev = Array.from({length: 40}, (_, i) => Math.sin(i/4)*30 + Math.cos(i/8)*50 + 100 + Math.random()*20);
    setElevationProfile(fakeElev);

    updateRouteProgress(map, cities, animationProgress, totalPathDist, lDists);""", elev_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
