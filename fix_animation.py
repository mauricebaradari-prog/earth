import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_effect = """  useEffect(() => {
    if (mapRef.current && routeInitializedRef.current) {
      updateRouteProgress(mapRef.current, cities, animationProgress, totalDistRef.current, legDistancesRef.current);
    }
  }, [animationProgress]);"""

new_effect = """  useEffect(() => {
    if (mapRef.current && routeInitializedRef.current) {
      const activeRoute = routes?.find(r => r.cities.length === cities.length && r.cities.every((c, idx) => c.id === cities[idx].id));
      const cs = (useGpsTrace || activeRoute?.forceStraight) && cities.length > 0 ? [cities[0], cities[cities.length-1]] : cities;
      updateRouteProgress(mapRef.current, cs, animationProgress, totalDistRef.current, legDistancesRef.current);
    }
  }, [animationProgress, cities, useGpsTrace, routes]);"""

content = content.replace(old_effect, new_effect)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
