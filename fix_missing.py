import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# We need to replace the marker building logic inside updateInactiveRoutes
old_logic = """    // Add start/end markers for inactive routes
    inactiveMarkersRef.current.forEach(m => m.remove());
    inactiveMarkersRef.current = [];
    import('maplibre-gl').then(({ Marker }) => {
      for (const route of routes) {
        const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
        if (isActive) continue;
        const startCity = route.cities[0];
        const endCity = route.cities[route.cities.length - 1];
        [startCity, endCity].forEach((city, idx) => {
          const el = document.createElement('div');
          el.innerHTML = getCityMarkerHTML(idx === 0 ? 'A' : 'B', city.name, idx === 0, idx === 1, route.id, false);
          el.style.opacity = '0.5';
          el.style.transition = 'opacity 0.2s';
          el.addEventListener('mouseenter', () => el.style.opacity = '1');
          el.addEventListener('mouseleave', () => el.style.opacity = '0.5');
          if (idx === 0) {
            el.style.cursor = 'pointer';
            el.addEventListener('click', () => {
              onPlayRoute && onPlayRoute(route.id);
            });
          }
          const marker = new Marker({ element: el, anchor: 'bottom' })
            .setLngLat([city.lng, city.lat])
            .addTo(map);
          inactiveMarkersRef.current.push(marker);
        });
      }
    });"""

new_logic = """    // Add start/end markers AND YouTube preview markers for inactive routes
    inactiveMarkersRef.current.forEach(m => m.remove());
    inactiveMarkersRef.current = [];
    import('maplibre-gl').then(({ Marker }) => {
      for (const route of routes) {
        const isActive = route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id);
        if (isActive) continue;
        
        // --- YOUTUBE PREVIEW MARKER ON EXACT ROUTE MIDPOINT ---
        let allRouteCoords: [number, number][] = [];
        for (let i = 0; i < route.cities.length - 1; i++) {
            const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
            const coords = osrmCacheRef.current[cacheKey] || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
            allRouteCoords = allRouteCoords.concat(coords);
        }
        
        if (allRouteCoords.length > 0) {
            const exactMidCoord = allRouteCoords[Math.floor(allRouteCoords.length / 2)];
            
            const ytEl = document.createElement('div');
            ytEl.className = 'route-preview-marker-container cursor-pointer';
            ytEl.style.zIndex = '40';
            
            const inner = document.createElement('div');
            inner.className = 'relative group transition-transform hover:scale-110 hover:z-50';
            inner.style.width = '90px';
            inner.style.height = '60px';
            inner.style.borderRadius = '8px';
            inner.style.overflow = 'hidden';
            inner.style.border = '2px solid rgba(255, 255, 255, 0.4)';
            inner.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.5)';
            
            const img = document.createElement('img');
            img.src = route.videoId ? `https://img.youtube.com/vi/${route.videoId}/mqdefault.jpg` : 'https://images.unsplash.com/photo-1542281286-9e0a16bb7366?auto=format&fit=crop&w=300&q=80';
            img.style.width = '100%';
            img.style.height = '100%';
            img.style.objectFit = 'cover';
            inner.appendChild(img);

            const overlay = document.createElement('div');
            overlay.className = 'absolute inset-0 bg-black/40 flex items-center justify-center opacity-70 group-hover:opacity-100 transition-opacity';
            overlay.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
            inner.appendChild(overlay);
            
            const title = document.createElement('div');
            title.className = 'absolute bottom-0 w-full bg-black/70 text-white text-[9px] font-bold px-1 py-0.5 truncate text-center';
            title.innerText = route.name || 'Route';
            inner.appendChild(title);
            
            ytEl.appendChild(inner);
            
            ytEl.onclick = (e) => {
              e.stopPropagation();
              if (onPlayRoute) onPlayRoute(route.id);
            };

            const ytMarker = new Marker({ element: ytEl })
              .setLngLat(exactMidCoord)
              .addTo(map);
            inactiveMarkersRef.current.push(ytMarker);
        }

        const startCity = route.cities[0];
        const endCity = route.cities[route.cities.length - 1];
        [startCity, endCity].forEach((city, idx) => {
          const el = document.createElement('div');
          el.innerHTML = getCityMarkerHTML(idx === 0 ? 'A' : 'B', city.name, idx === 0, idx === 1, route.id, false);
          el.style.opacity = '0.5';
          el.style.transition = 'opacity 0.2s';
          el.addEventListener('mouseenter', () => el.style.opacity = '1');
          el.addEventListener('mouseleave', () => el.style.opacity = '0.5');
          if (idx === 0) {
            el.style.cursor = 'pointer';
            el.addEventListener('click', () => {
              onPlayRoute && onPlayRoute(route.id);
            });
          }
          const marker = new Marker({ element: el, anchor: 'bottom' })
            .setLngLat([city.lng, city.lat])
            .addTo(map);
          inactiveMarkersRef.current.push(marker);
        });
      }
    });"""

content = content.replace(old_logic, new_logic)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
