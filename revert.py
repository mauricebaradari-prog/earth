import re

content = """'use client';

import React, { useEffect, useRef, useState } from 'react';
import maplibregl, { Map as MaplibreMap, GeoJSONSource } from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';
import { City, VehicleConfig, MapStyleId } from '@/hooks/useEditorState';
import { greatCircleArc } from '@/lib/geo';

interface GlobeMapProps {
  cities: City[];
  vehicle: VehicleConfig;
  mapStyle: MapStyleId;
  animationProgress: number; // 0-1
  isAnimating: boolean;
  globeAtmosphere: boolean;
  routeColor: string;
  routeWidth: number;
  durationSeconds: number;
  onPoint1Projected?: (x: number, y: number) => void;
  showElevation?: boolean;
  onSeek?: (progress: number) => void;
}

export default function GlobeMap({
  cities,
  vehicle,
  mapStyle,
  animationProgress,
  isAnimating,
  globeAtmosphere,
  routeColor,
  routeWidth,
  durationSeconds,
  onPoint1Projected,
  showElevation = true,
  onSeek
}: GlobeMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MaplibreMap | null>(null);
  const prevStyleRef = useRef<string | null>(null);
  const routeInitializedRef = useRef(false);
  const markersRef = useRef<maplibregl.Marker[]>([]);
  
  const renderPassRef = useRef<number>(0);
  const [svgPath, setSvgPath] = React.useState<string>('');
  const [fullSvgPath, setFullSvgPath] = React.useState<string>('');
  const [vehicleDot, setVehicleDot] = React.useState<{x:number,y:number}|null>(null);
  const [distanceBadge, setDistanceBadge] = React.useState<{x:number, y:number, text: string, text2: string}|null>(null);
  const [elevationProfile, setElevationProfile] = React.useState<number[] | null>(null);
  
  const osrmCacheRef = useRef<Record<string, [number, number][]>>({});
  const midLngLatRef = useRef<[number, number] | null>(null);
  const vehicleLngLatRef = useRef<[number, number] | null>(null);
  const totalDistRef = useRef<number>(0);
  const legDistancesRef = useRef<number[]>([]);
  
  const routeCoordsRef = useRef<GeoJSON.Feature[]>([]);

  // ── 1. Init Map ─────────────────────────────────────────────────────────────
  useEffect(() => {
    if (!containerRef.current) return;
    if (!mapRef.current) {
      let mapInstance: MaplibreMap;

      const styleUrl =
        mapStyle === 'streets'
          ? 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
          : mapStyle === 'terrain'
          ? 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
          : 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

      const map = new maplibregl.Map({
        container: containerRef.current,
        style: styleUrl,
        center: [cities[0]?.lng || 0, cities[0]?.lat || 0],
        zoom: 4,
        pitch: 45,
        interactive: true,
      });

      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }));
      mapInstance = map;
      mapRef.current = map;
      prevStyleRef.current = mapStyle;

      const updateSvgOverlay = () => {
        try {
          if (!mapRef.current) return;
          
          let fullPts: [number, number][] = [];
          if (mapRef.current.getSource('route')) {
             const data = (mapRef.current.getSource('route') as GeoJSONSource)._data as GeoJSON.FeatureCollection;
             if (data && data.features) {
                data.features.forEach((feat) => {
                  if (feat.geometry.type === 'LineString') {
                    fullPts = fullPts.concat(feat.geometry.coordinates as [number, number][]);
                  }
                });
             }
          }

          const screenPts = [];
          for (const c of fullPts) {
             const p = mapRef.current.project([c[0], c[1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);

          const pts = [];
          routeCoordsRef.current.forEach((feat) => {
            if (feat.geometry.type === 'LineString') {
               const coords = feat.geometry.coordinates as [number, number][];
               for (const c of coords) {
                 const p = mapRef.current.project([c[0], c[1]]);
                 pts.push(`${p.x},${p.y}`);
               }
            }
          });
          if (pts.length > 0) {
            setSvgPath(`M ${pts.join(' L ')}`);
          }

          if (vehicleLngLatRef.current) {
            const p = mapRef.current.project(vehicleLngLatRef.current);
            setVehicleDot({ x: p.x, y: p.y });
          }

          if (midLngLatRef.current) {
             const p = mapRef.current.project(midLngLatRef.current);
             const distKm = (totalDistRef.current / 1000).toFixed(0);
             const m = Math.floor(durationSeconds / 60);
             const s = durationSeconds % 60;
             setDistanceBadge({
               x: p.x, y: p.y,
               text: `${distKm} km`,
               text2: `${m}m ${s}s`
             });
          }
        } catch (e) {
           console.error(e);
        }
      };
      (window as any)._updateSvgOverlay = updateSvgOverlay;

      map.on('move', updateSvgOverlay);
      map.on('zoom', updateSvgOverlay);
      map.on('pitch', updateSvgOverlay);
      map.on('render', updateSvgOverlay);

      map.once('style.load', () => {
        (map as any).setProjection({ type: 'globe' });
        initRouteLayers(map, routeColor, routeWidth);
        routeInitializedRef.current = true;
        updateRouteData(map, 0);
        rebuildMarkers(map, cities);
      });

      return () => {
        map.remove();
        mapRef.current = null;
      };
    }
  }, []);

  function initRouteLayers(map: MaplibreMap, color: string, width: number) {
    if (!map.getSource('route')) {
      map.addSource('route', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
    
    if (!map.getLayer('route-glow')) {
      map.addLayer({
        id: 'route-glow',
        type: 'line',
        source: 'route',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': 12,
          'line-opacity': 0.5,
          'line-color': color
        }
      });
    }
    if (!map.getLayer('route-line')) {
      map.addLayer({
        id: 'route-line',
        type: 'line',
        source: 'route',
        layout: { 'line-cap': 'round', 'line-join': 'round' },
        paint: {
          'line-width': width * 1.5 + 1,
          'line-opacity': 1,
          'line-color': color
        }
      });
    }
  }

  // ── 2. Style & Atmosphere update ─────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map) return;

    if (globeAtmosphere) {
      map.setFog({
        color: 'rgba(255, 255, 255, 0.2)',
        'high-color': 'rgba(0, 0, 0, 0.8)',
        'space-color': 'rgba(0, 0, 0, 1)'
      } as any);
    } else {
      map.setFog(null as any);
    }

    if (mapStyle !== prevStyleRef.current) {
      const styleUrl =
        mapStyle === 'streets'
          ? 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json'
          : mapStyle === 'terrain'
          ? 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json'
          : 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

      prevStyleRef.current = mapStyle;
      map.setStyle(styleUrl);
      map.once('style.load', () => {
        (map as any).setProjection({ type: 'globe' });
        if (globeAtmosphere) {
           map.setFog({
             color: 'rgba(255, 255, 255, 0.2)',
             'high-color': 'rgba(0, 0, 0, 0.8)',
             'space-color': 'rgba(0, 0, 0, 1)'
           } as any);
        }
        initRouteLayers(map, routeColor, routeWidth);
        updateRouteData(map, 0); // Reset to full line
        rebuildMarkers(map, cities);
      });
    }
  }, [mapStyle, globeAtmosphere]);

  // ── 3. Cities update ─────────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    renderPassRef.current += 1;
    updateRouteData(map, renderPassRef.current);
    rebuildMarkers(map, cities);

    if (cities.length >= 2) {
      const lats = cities.map((c) => c.lat);
      const lngs = cities.map((c) => c.lng);
      const minLat = Math.min(...lats);
      const maxLat = Math.max(...lats);
      const minLng = Math.min(...lngs);
      const maxLng = Math.max(...lngs);
      map.fitBounds(
        [[minLng, minLat], [maxLng, maxLat]],
        { padding: 100, duration: 1200 }
      );
    }
  }, [cities]);

  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route')) return;
    
    let totalPathDist = 0;
    const lDists: number[] = [];
    const allFeatures: GeoJSON.Feature[] = [];

    for (let i = 0; i < cities.length - 1; i++) {
      let routeCoords = null;
      try {
        if (renderPassRef.current !== passId) return;
        const cacheKey = `${cities[i].id}-${cities[i+1].id}`;
        if (osrmCacheRef.current[cacheKey]) {
           routeCoords = osrmCacheRef.current[cacheKey];
        } else {
           const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${cities[i].lng},${cities[i].lat};${cities[i+1].lng},${cities[i+1].lat}?geometries=geojson`);
           const data = await res.json();
           if (data.routes && data.routes[0]) {
             routeCoords = data.routes[0].geometry.coordinates;
           }
        }
      } catch (e) {
        console.warn("OSRM fetch failed, using fallback");
      }

      const finalCoords = routeCoords || greatCircleArc(cities[i], cities[i + 1], 120);
      osrmCacheRef.current[`${cities[i].id}-${cities[i+1].id}`] = finalCoords;

      let legDist = 0;
      for (let j = 0; j < finalCoords.length - 1; j++) {
        legDist += distance(finalCoords[j], finalCoords[j+1]);
      }
      lDists.push(legDist);
      totalPathDist += legDist;

      allFeatures.push({
        type: 'Feature',
        properties: {},
        geometry: { type: 'LineString', coordinates: finalCoords }
      });
    }

    if (allFeatures.length > 0) {
      const allCoords = allFeatures.flatMap(f => (f.geometry as any).coordinates);
      if (allCoords.length > 0) {
        midLngLatRef.current = allCoords[Math.floor(allCoords.length / 2)];
      }
    }
    
    totalDistRef.current = totalPathDist;
    legDistancesRef.current = lDists;
    
    if (map.getSource('route')) {
      (map.getSource('route') as GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: allFeatures,
      });
    }
    
    // Simulate elevation profile
    const fakeElev = Array.from({length: 40}, (_, i) => Math.sin(i/4)*30 + Math.cos(i/8)*50 + 100 + Math.random()*20);
    setElevationProfile(fakeElev);

    updateRouteProgress(map, cities, animationProgress, totalPathDist, lDists);
  }

  // ── 4. Animation progress update ─────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    
    // Camera follow logic
    if (isAnimating && cities.length >= 2 && vehicleLngLatRef.current) {
       const curZoom = map.getZoom();
       if (curZoom < 10) {
         map.flyTo({
           center: vehicleLngLatRef.current,
           zoom: 12,
           pitch: 60,
           duration: 1000,
           essential: true
         });
       } else {
         const bearing = headingOnPath(routeCoordsRef.current.flatMap(f => (f.geometry as any).coordinates), animationProgress);
         map.easeTo({
           center: vehicleLngLatRef.current,
           bearing: bearing,
           pitch: 60,
           duration: 300,
           easing: (t) => t
         });
       }
    }

    updateRouteProgress(map, cities, animationProgress, totalDistRef.current, legDistancesRef.current);
  }, [animationProgress, isAnimating]);

  // ── 5. Route Color update ────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    if (map.getLayer('route-glow')) {
      map.setPaintProperty('route-glow', 'line-color', routeColor);
    }
    if (map.getLayer('route-line')) {
      map.setPaintProperty('route-line', 'line-color', routeColor);
    }
    if (map.getLayer('route-inactive-glow')) {
      map.setPaintProperty('route-inactive-glow', 'line-color', routeColor);
    }
  }, [routeColor]);


  function updateRouteProgress(
    map: MaplibreMap,
    cs: City[],
    progress: number,
    totalDist: number,
    legDists: number[]
  ) {
    if (!map.getSource('route')) return;

    let remaining = progress;
    let vehiclePoint = cs[0] ? [cs[0].lng, cs[0].lat] : [0,0];
    const newActiveFeatures: GeoJSON.Feature[] = [];

    for (let i = 0; i < cs.length - 1; i++) {
      const legFrac = legDists[i] / totalDist;
      const legProgress = Math.min(1, remaining / legFrac);
      remaining -= legFrac;

      const fullArc = osrmCacheRef.current[`${cs[i].id}-${cs[i+1].id}`] || greatCircleArc(cs[i], cs[i + 1], 120);
      const exactIdx = legProgress * (fullArc.length - 1);
      const numCompletePoints = Math.floor(exactIdx) + 1;
      
      const partialArc = fullArc.slice(0, numCompletePoints);
      
      if (legProgress > 0 && legProgress < 1 && numCompletePoints < fullArc.length) {
         const p1 = fullArc[numCompletePoints - 1];
         const p2 = fullArc[numCompletePoints];
         const frac = exactIdx - (numCompletePoints - 1);
         vehiclePoint = [
           p1[0] + (p2[0] - p1[0]) * frac,
           p1[1] + (p2[1] - p1[1]) * frac
         ];
         partialArc.push(vehiclePoint as [number, number]);
      } else if (legProgress === 1) {
         vehiclePoint = fullArc[fullArc.length - 1];
      }

      if (partialArc.length > 1) {
         newActiveFeatures.push({
           type: 'Feature',
           properties: {},
           geometry: { type: 'LineString', coordinates: partialArc }
         });
      }

      if (remaining <= 0) break;
    }

    vehicleLngLatRef.current = vehiclePoint as [number, number];
    routeCoordsRef.current = newActiveFeatures;

    if ((window as any)._updateSvgOverlay) {
      (window as any)._updateSvgOverlay();
    }
  }

  function rebuildMarkers(map: MaplibreMap, cs: City[]) {
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];
    import('maplibre-gl').then(({ Marker }) => {
      cs.forEach((city, i) => {
        if (i !== 0 && i !== cs.length - 1) return;
        const label = i === 0 ? 'A' : 'B';
        const el = document.createElement('div');
        el.innerHTML = getCityMarkerHTML(label, city.name, i === 0, i === cs.length - 1);
        const marker = new Marker({ element: el, anchor: 'bottom' })
          .setLngLat([city.lng, city.lat])
          .addTo(map);
        markersRef.current.push(marker);
      });
    });
  }

  return (
    <div className="w-full h-full relative" ref={containerRef}>
      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <path d={fullSvgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeOpacity={0.3} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
      </svg>
      {vehicleDot && (
        <div 
          className="absolute w-3 h-3 bg-white rounded-full shadow-md pointer-events-none z-20 border-[2px]"
          style={{
            left: vehicleDot.x,
            top: vehicleDot.y,
            borderColor: routeColor,
            transform: 'translate(-50%, -50%)',
          }}
        />
      )}
      {distanceBadge && (
        <div 
          className=""
          style={{
          position: 'absolute',
          left: distanceBadge.x,
          top: distanceBadge.y,
          transform: 'translate(-50%, -50%)',
          zIndex: 30,
          pointerEvents: 'none',
        }}>
          <div style={{
            background: 'rgba(26,26,26,0.9)',
            border: '1px solid rgba(255,255,255,0.1)',
            backdropFilter: 'blur(8px)',
            borderRadius: '12px',
            padding: '4px 10px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
            transform: 'translateY(-30px)',
          }}>
             <span style={{ color: '#fff', fontSize: '13px', fontWeight: 700, fontFamily: 'sans-serif' }}>{distanceBadge.text}</span>
             <span style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif', marginTop: '1px' }}>{distanceBadge.text2}</span>
          </div>
        </div>
      )}
      
      {showElevation && elevationProfile && (
        <div style={{ position: 'absolute', top: 20, right: 20, zIndex: 40, width: 320, background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }}>
            <div>
              <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: '0 0 4px 0', fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Elevation Profile</h3>
              <div style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>{(totalDistRef.current / 1000).toFixed(0)} KM</span>
                <span style={{ color: '#4b5563' }}>•</span>
                <span>{Math.floor(durationSeconds / 60)}M {durationSeconds % 60}S</span>
              </div>
            </div>
            <button style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer', padding: '4px' }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M4 8h16M4 16h16"/></svg>
            </button>
          </div>
          
          <div style={{ position: 'relative', height: '60px', width: '100%' }}>
            <div style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', pointerEvents: 'none' }}>
              <div style={{ borderBottom: '1px dashed rgba(255,255,255,0.1)', height: '1px', width: '100%' }} />
              <div style={{ borderBottom: '1px dashed rgba(255,255,255,0.1)', height: '1px', width: '100%' }} />
              <div style={{ borderBottom: '1px solid rgba(255,255,255,0.2)', height: '1px', width: '100%' }} />
            </div>
            <div style={{ position: 'absolute', left: 0, bottom: '-16px', color: '#6b7280', fontSize: '9px', fontWeight: 600, fontFamily: 'sans-serif' }}>
              0m
            </div>
            <div style={{ position: 'absolute', left: '-2px', bottom: '2px', color: '#fff', fontSize: '9px', fontWeight: 700, fontFamily: 'sans-serif', background: 'rgba(0,0,0,0.5)', padding: '2px 4px', borderRadius: '4px' }}>
              69m
            </div>
            
            <div style={{ width: '100%', height: '100%', position: 'relative' }}>
              <div style={{ position: 'absolute', left: 0, bottom: 0, width: '100%', height: '100%' }}>
                {(() => {
                  const max = Math.max(...elevationProfile);
                  const min = Math.min(...elevationProfile);
                  const range = max - min || 1;
                  const pts = elevationProfile.map((v, i) => `${(i / (elevationProfile.length - 1)) * 100},${100 - ((v - min) / range) * 100}`);
                  const path = `M 0,100 L ${pts.map(p => { const [x,y] = p.split(','); return `${x},${y}`; }).join(' L ')} L 100,100 Z`;
                  
                  return (
                    <svg 
                      width="100%" 
                      height="100%" 
                      viewBox="0 0 100 100" 
                      preserveAspectRatio="none" 
                      style={{ overflow: 'visible', cursor: onSeek ? 'pointer' : 'default', pointerEvents: 'auto' }}
                      onClick={(e) => {
                        if (!onSeek) return;
                        const rect = e.currentTarget.getBoundingClientRect();
                        let p = (e.clientX - rect.left) / rect.width;
                        p = Math.max(0, Math.min(1, p));
                        onSeek(p);
                      }}
                    >
                      <defs>
                        <linearGradient id="elevGrad" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.3} />
                          <stop offset="100%" stopColor={routeColor} stopOpacity={0.6} />
                        </linearGradient>
                        <linearGradient id="elevLineGrad" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#FFFFFF" />
                          <stop offset="100%" stopColor={routeColor} />
                        </linearGradient>
                      </defs>
                      <path d={path} fill="url(#elevGrad)" opacity={0.5} />
                      <path d={path.replace(' L 100,100 Z', '').replace('M 0,100 L ', 'M ')} fill="none" stroke="url(#elevLineGrad)" strokeWidth="3" vectorEffect="non-scaling-stroke" strokeLinecap="round" strokeLinejoin="round" />
                    </svg>
                  );
                })()}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function distance(p1: [number, number], p2: [number, number]) {
  const R = 6371e3;
  const φ1 = (p1[1] * Math.PI) / 180;
  const φ2 = (p2[1] * Math.PI) / 180;
  const Δφ = ((p2[1] - p1[1]) * Math.PI) / 180;
  const Δλ = ((p2[0] - p1[0]) * Math.PI) / 180;
  const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) + Math.cos(φ1) * Math.cos(φ2) * Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function getCityMarkerHTML(label: string, name: string, isFirst: boolean, isLast: boolean): string {
  let color = '#4ade80';
  let innerHtml = label;
  
  if (isFirst) {
    color = '#ffffff';
    innerHtml = `
      <svg width="20" height="20" viewBox="0 0 24 24" fill="#111">
        <path d="M19.44,9.03L15.41,5H11v2h3.59l2,2H5C2.24,9,0,11.24,0,14s2.24,5,5,5c2.46,0,4.5-1.75,4.9-4h4.2 c0.4,2.25,2.44,4,4.9,4c2.76,0,5-2.24,5-5C24,11.69,21.99,9.67,19.44,9.03z M5,17c-1.66,0-3-1.34-3-3s1.34-3,3-3s3,1.34,3,3 S6.66,17,5,17z M19,17c-1.66,0-3-1.34-3-3s1.34-3,3-3s3,1.34,3,3S20.66,17,19,17z M10.82,6.5L9.56,4.8C9.07,5.52,8.18,6,7.2,6H4V8h3.2 C7.9,8,8.5,7.5,8.81,6.8L9.26,6H11V8h2L10.82,6.5z"/>
      </svg>
    `;
  } else if (isLast) {
    color = '#ffffff';
    innerHtml = `
      <svg width="18" height="18" viewBox="0 0 24 24" style="transform: translateX(1px)">
        <rect x="4" y="2" width="2.5" height="20" fill="#111" rx="1" />
        <rect x="6.5" y="3" width="12" height="12" fill="none" stroke="#111" stroke-width="1.5" />
        <rect x="6.5" y="3" width="4" height="4" fill="#111" />
        <rect x="14.5" y="3" width="4" height="4" fill="#111" />
        <rect x="10.5" y="7" width="4" height="4" fill="#111" />
        <rect x="6.5" y="11" width="4" height="4" fill="#111" />
        <rect x="14.5" y="11" width="4" height="4" fill="#111" />
      </svg>
    `;
  } else {
    color = '#CCFF00';
  }
  
  return `
    <div style="display:flex; flex-direction:column; align-items:center; transform:translateY(-4px);">
      <div style="background:${color}; color:#111; font-weight:bold; font-family:sans-serif; width:32px; height:32px; display:flex; align-items:center; justify-content:center; border-radius:50%; border:3px solid #1a1a1a; box-shadow:0 4px 6px rgba(0,0,0,0.3); z-index:10;">
        ${innerHtml}
      </div>
      <div style="margin-top:4px; background:#1a1a1a; color:#f3f4f6; padding:2px 8px; border-radius:4px; font-size:12px; font-family:sans-serif; font-weight:600; border:1px solid #333; box-shadow:0 2px 4px rgba(0,0,0,0.3); white-space:nowrap;">
        ${name}
      </div>
    </div>
  `;
}

function headingOnPath(path: [number, number][], t: number) {
  if (!path || path.length < 2) return 0;
  let exactIdx = t * (path.length - 1);
  if (exactIdx < path.length - 2) exactIdx += 0.5;
  const idx = Math.min(Math.floor(exactIdx), path.length - 2);
  const p1 = path[idx];
  const p2 = path[idx + 1];
  return Math.atan2(p2[0] - p1[0], p2[1] - p1[1]) * (180 / Math.PI);
}
"""

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
