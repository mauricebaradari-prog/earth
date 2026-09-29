import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_code = """    let didFetch = false;
    const fetchPromises = [];
    
    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      const activeRoute = routes?.find(r => r.cities.length === cities.length && r.cities.every((c, idx) => c.id === cities[idx].id));
      if (!osrmCacheRef.current[cacheKey] && !activeRoute?.forceStraight) {"""

new_code = """    let didFetch = false;
    const fetchPromises = [];
    
    const activeRoute = routes?.find(r => r.cities.length === cities.length && r.cities.every((c, idx) => c.id === cities[idx].id));

    for (let i = 0; i < cities.length - 1; i++) {
      const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
      if (!osrmCacheRef.current[cacheKey] && !activeRoute?.forceStraight) {"""

content = content.replace(old_code, new_code)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
