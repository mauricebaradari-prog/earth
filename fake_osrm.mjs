const wps = [
  [32.6290, 34.6657],
  [32.6450, 34.6600],
  [32.6650, 34.6560],
  [32.6800, 34.6600],
  [32.6962, 34.6746]
];
// If I use these as waypoints in GlobeMap, and OSRM fails or detours, it will fallback to straight lines between them!
// Wait, if I just clear OSRM cache for these pairs and force them to fail? No, OSRM will succeed and route via the highway (looping).
// How to force GlobeMap to NOT use OSRM for these points?
