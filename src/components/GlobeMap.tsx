'use client';

import React, { useRef, useEffect } from 'react';
import { GripHorizontal } from 'lucide-react';
//  { useEffect, useRef, useState } from 'react';
import * as maplibregl from 'maplibre-gl';
import { Rnd } from 'react-rnd';
type MaplibreMap = maplibregl.Map;
type GeoJSONSource = maplibregl.GeoJSONSource;
import { City, VehicleConfig, MapStyleId } from '@/hooks/useEditorState';
import { greatCircleArc } from '@/lib/geo';

function getDistance(p1: [number, number], p2: [number, number]) {
  const R = 6371e3;
  const rad = Math.PI / 180;
  const lat1 = p1[1] * rad;
  const lat2 = p2[1] * rad;
  const dLat = (p2[1] - p1[1]) * rad;
  const dLon = (p2[0] - p1[0]) * rad;
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) + Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
  return R * c;
}


interface GlobeMapProps {
  cities: City[];
  routes?: { id: string; name: string; cities: City[] }[];
  vehicle: VehicleConfig;
  mapStyle: MapStyleId;
  animationProgress: number; // 0-1
  isAnimating: boolean;
  cameraMode: 'static' | 'follow' | 'orbit';
  globeAtmosphere: boolean;
  routeColor: string;
  routeWidth: number;
  durationSeconds: number;
  onPoint1Projected?: (x: number, y: number) => void;
  showElevation?: boolean;
  onSeek?: (progress: number) => void;
  activeWindow?: 'video' | 'elevation' | null;
  setActiveWindow?: (w: 'video' | 'elevation') => void;
}

export default function GlobeMap({
  cities,
  routes,
  vehicle,
  mapStyle,
  animationProgress,
  isAnimating,
  cameraMode,
  globeAtmosphere,
  routeColor,
  routeWidth,
  durationSeconds,
  onPoint1Projected,
  showElevation = true,
  onSeek,
  activeWindow,
  setActiveWindow
}: GlobeMapProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<MaplibreMap | null>(null);
  const prevStyleRef = useRef<string | null>(null);
  const routeInitializedRef = useRef(false);
  const markersRef = useRef<maplibregl.Marker[]>([]);
  const initialCameraRef = useRef<{center: {lng: number, lat: number}, zoom: number, pitch: number, bearing: number, timestamp: number} | null>(null);
  
  const renderPassRef = useRef<number>(0);
      const [vehicleDot, setVehicleDot] = React.useState<{x:number,y:number}|null>(null);
  const [distanceBadge, setDistanceBadge] = React.useState<{x:number, y:number, text: string, text2: string}|null>(null);
  const [elevationProfile, setElevationProfile] = React.useState<number[] | null>(null);
  const [fullSvgPath, setFullSvgPath] = React.useState<string>('');
  const [svgPath, setSvgPath] = React.useState<string>('');
  
  const animProgressRef = useRef(animationProgress);
  const durationRef = useRef(durationSeconds);
  
  useEffect(() => {
    animProgressRef.current = animationProgress;
    durationRef.current = durationSeconds;
  }, [animationProgress, durationSeconds]);

  const osrmCacheRef = useRef<Record<string, [number, number][]>>({});
  const osrmDistCacheRef = useRef<Record<string, number[]>>({});
  const midLngLatRef = useRef<[number, number] | null>(null);
  const vehicleLngLatRef = useRef<[number, number] | null>(null);
  const totalDistRef = useRef<number>(0);
  const legDistancesRef = useRef<number[]>([]);
  
  const routeCoordsRef = useRef<GeoJSON.Feature[]>([]);
  const fullRouteCoordsRef = useRef<[number, number][]>([]);

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
          : mapStyle === 'satellite'
          ? {
              version: 8 as 8,
              sources: {
                'satellite': {
                  type: 'raster' as 'raster',
                  tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
                  tileSize: 256
                }
              },
              layers: [
                {
                  id: 'background',
                  type: 'background' as 'background',
                  paint: {
                    'background-color': '#000000'
                  }
                },
                {
                  id: 'satellite-layer',
                  type: 'raster' as 'raster',
                  source: 'satellite',
                  minzoom: 0,
                  maxzoom: 19
                }
              ]
            }
          : 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';

      const map = new maplibregl.Map({
        container: containerRef.current,
        style: styleUrl,
        center: [cities[0]?.lng || 0, cities[0]?.lat || 0],
        zoom: 4,
        pitch: 45,
        interactive: true,
      });

      map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
      mapInstance = map;
      mapRef.current = map;
      prevStyleRef.current = mapStyle;

      const updateSvgOverlay = () => {
        try {
          if (!mapRef.current) return;
          
          let fullPts = fullRouteCoordsRef.current;


          const currentProgress = animProgressRef.current;
          const currentDuration = durationRef.current;
          if (currentProgress === 0 && fullPts.length > 0 && onPoint1Projected) {
             const p1 = mapRef.current.project([fullPts[0][0], fullPts[0][1]]);
             // Only call if it moved significantly to avoid spam
             if (!(window as any)._lastP1 || Math.abs((window as any)._lastP1.x - p1.x) > 10 || Math.abs((window as any)._lastP1.y - p1.y) > 10) {
               (window as any)._lastP1 = { x: p1.x, y: p1.y };
               onPoint1Projected(p1.x, p1.y);
             }
          }
          const screenPts = [];
          for (const c of fullPts) {
             if (!mapRef.current) continue;
                 const p = mapRef.current.project([c[0], c[1]]);
             screenPts.push(`${p.x},${p.y}`);
          }
          if (screenPts.length > 0) setFullSvgPath(`M ${screenPts.join(' L ')}`);

          const pts: string[] = [];
          routeCoordsRef.current.forEach((feat) => {
            if (feat.geometry.type === 'LineString') {
               const coords = feat.geometry.coordinates as [number, number][];
               for (const c of coords) {
                 if (!mapRef.current) continue;
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
             
             const currentProgress = animProgressRef.current;
             const currentDuration = durationRef.current;
             
             let displayDist = totalDistRef.current / 1000;
             let displaySecs = currentDuration;
             
             if (currentProgress > 0) {
               displayDist = displayDist * currentProgress;
               displaySecs = currentDuration * (1 - currentProgress);
             }
             
             const distKm = displayDist.toFixed(0);
             const m = Math.floor(displaySecs / 60);
             const s = Math.floor(displaySecs % 60);
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
        try {
          if (globeAtmosphere && (map as any).setFog) {
             (map as any).setFog({
               color: 'rgba(255, 255, 255, 0.2)',
               'high-color': 'rgba(0, 0, 0, 0.8)',
               'space-color': 'rgba(0, 0, 0, 1)'
             });
          }
        } catch (e) {}

        initRouteLayers(map, routeColor, routeWidth);
        routeInitializedRef.current = true;
        updateRouteData(map, 0);
        rebuildMarkers(map, cities);
        updateInactiveRoutes(map);
        if (cities.length >= 2) {
          const lats = cities.map((c) => c.lat);
          const lngs = cities.map((c) => c.lng);
          const minLat = Math.min(...lats);
          const maxLat = Math.max(...lats);
          const minLng = Math.min(...lngs);
          const maxLng = Math.max(...lngs);
          map.fitBounds(
            [
              [minLng, minLat],
              [maxLng, maxLat],
            ],
            { padding: 50, duration: 1200, maxZoom: 13 }
          );
        }
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
    if (!map.getSource('inactive-routes')) {
      map.addSource('inactive-routes', {
        type: 'geojson',
        data: { type: 'FeatureCollection', features: [] }
      });
    }
    if (!map.getLayer('inactive-routes-line')) {
      map.addLayer({
        id: 'inactive-routes-line',
        type: 'line',
        source: 'inactive-routes',
        layout: {
          'line-join': 'round',
          'line-cap': 'round',
        },
        paint: {
          'line-color': '#ffffff',
          'line-width': width,
          'line-opacity': 0.5,
          'line-dasharray': [2, 2],
        },
      });
    }
  }

  // ── 2. Style update ──────────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (map && mapStyle && routeInitializedRef.current) {
      let styleUrl: string | maplibregl.StyleSpecification | undefined = undefined;
      
      if (mapStyle === 'streets') styleUrl = 'https://basemaps.cartocdn.com/gl/positron-gl-style/style.json';
      else if (mapStyle === 'terrain') styleUrl = 'https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json';
      else if (mapStyle === 'satellite') {
         styleUrl = {
              version: 8 as 8,
              sources: {
                'satellite': {
                  type: 'raster' as 'raster',
                  tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
                  tileSize: 256
                }
              },
              layers: [
                {
                  id: 'background',
                  type: 'background' as 'background',
                  paint: {
                    'background-color': '#000000'
                  }
                },
                {
                  id: 'satellite-layer',
                  type: 'raster',
                  source: 'satellite',
                  minzoom: 0,
                  maxzoom: 19
                }
              ]
         };
      } else {
         styleUrl = 'https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json';
      }

      map.setStyle(styleUrl);
      map.once('style.load', () => {
        (map as any).setProjection({ type: 'globe' });
        try {
          if (globeAtmosphere && (map as any).setFog) {
             (map as any).setFog({
               color: 'rgba(255, 255, 255, 0.2)',
               'high-color': 'rgba(0, 0, 0, 0.8)',
               'space-color': 'rgba(0, 0, 0, 1)'
             });
          }
        } catch (e) {}

        initRouteLayers(map, routeColor, routeWidth);
        updateRouteData(map, 0); // Reset to full line
        rebuildMarkers(map, cities);
      });
    }
  }, [mapStyle, globeAtmosphere]);

  // ── Fetch Inactive Routes ──────────────────────────────────────────────────

  async function updateInactiveRoutes(map: MaplibreMap) {
    if (!routes) return;
    const allFeatures: GeoJSON.Feature[] = [];
    
    for (const route of routes) {
      if (route.cities.length === cities.length && route.cities.every((c, i) => c.id === cities[i].id)) continue;
      
      for (let i = 0; i < route.cities.length - 1; i++) {
        const cacheKey = `${route.cities[i].id}-${route.cities[i+1].id}`;
        let coords = osrmCacheRef.current[cacheKey];
        if (!coords) {
          try {
             const res = await fetch(`https://router.project-osrm.org/route/v1/driving/${route.cities[i].lng},${route.cities[i].lat};${route.cities[i+1].lng},${route.cities[i+1].lat}?geometries=geojson`);
             const data = await res.json();
             if (data.routes && data.routes[0]) {
               coords = data.routes[0].geometry.coordinates;
               osrmCacheRef.current[cacheKey] = coords;
             }
          } catch(e) {}
        }
        const finalCoords = coords || greatCircleArc(route.cities[i], route.cities[i + 1], 120);
        allFeatures.push({
          type: 'Feature',
          properties: {},
          geometry: { type: 'LineString', coordinates: finalCoords }
        });
      }
    }
    if (map.getSource('inactive-routes')) {
      (map.getSource('inactive-routes') as GeoJSONSource).setData({
        type: 'FeatureCollection',
        features: allFeatures,
      });
    }
  }

  useEffect(() => {
    if (mapRef.current && routeInitializedRef.current) {
      updateInactiveRoutes(mapRef.current);
    }
  }, [routes, cities, mapStyle]);


  // ── 3. Cities update ─────────────────────────────────────────────────────────
  useEffect(() => {
    const map = mapRef.current;
    if (!map || !routeInitializedRef.current) return;
    renderPassRef.current += 1;
    legDistancesRef.current = [];
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
        [
          [minLng, minLat],
          [maxLng, maxLat],
        ],
        { padding: 50, duration: 1200, maxZoom: 13 }
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
      fullRouteCoordsRef.current = allCoords;
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
    
    updateRouteProgress(map, cities, animProgressRef.current, totalPathDist, lDists);
    if ((window as any)._updateSvgOverlay) {
      (window as any)._updateSvgOverlay();
    }
    

    
    // Fetch elevation profile
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
  }

  function updateRouteProgress(
    map: MaplibreMap,
    cs: City[],
    progress: number,
    totalDist: number,
    legDists: number[]
  ) {
    
    if (!map.getSource('route') || legDists.length !== cs.length - 1) return;

    let remaining = progress;
    let vehiclePoint = (progress === 0 && midLngLatRef.current) ? midLngLatRef.current : (cs[0] ? [cs[0].lng, cs[0].lat] : [0,0]);
    const newActiveFeatures: GeoJSON.Feature[] = [];

    for (let i = 0; i < cs.length - 1; i++) {
      const legFrac = legDists[i] / totalDist;
      const legProgress = Math.min(1, remaining / legFrac);
      remaining -= legFrac;

      const cacheKey = `${cs[i].id}-${cs[i+1].id}`;
      const fullArc = osrmCacheRef.current[cacheKey] || greatCircleArc(cs[i], cs[i + 1], 120);
      
      let accDists = osrmDistCacheRef.current[cacheKey];
      if (!accDists) {
         accDists = [0];
         let total = 0;
         for(let k = 1; k < fullArc.length; k++) {
            total += getDistance(fullArc[k-1], fullArc[k]);
            accDists.push(total);
         }
         osrmDistCacheRef.current[cacheKey] = accDists;
      }
      
      const arcTotalDist = accDists[accDists.length - 1];
      const targetDist = legProgress * arcTotalDist;
      
      let numCompletePoints = 1;
      for (let k = 1; k < accDists.length; k++) {
         if (accDists[k] <= targetDist) {
            numCompletePoints = k + 1;
         } else {
            break;
         }
      }
      
      const partialArc = fullArc.slice(0, numCompletePoints);
      
      if (legProgress > 0 && legProgress < 1 && numCompletePoints < fullArc.length) {
         const p1 = fullArc[numCompletePoints - 1];
         const p2 = fullArc[numCompletePoints];
         const d1 = accDists[numCompletePoints - 1];
         const d2 = accDists[numCompletePoints];
         const frac = (d2 - d1) === 0 ? 0 : (targetDist - d1) / (d2 - d1);
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

    
    if (cameraMode !== 'static' && progress > 0 && progress < 1) {
      let targetBearing = map.getBearing();
      if (cameraMode === 'orbit') {
        targetBearing = progress * 360;
      } else if (cameraMode === 'follow') {
        targetBearing = headingOnPath(fullRouteCoordsRef.current, progress);
      }
      
      const targetZoom = Math.max(map.getZoom(), 8);
      const targetPitch = Math.max(map.getPitch(), 45);
      const targetCenter = vehiclePoint as [number, number];
      
      const TRANSITION_DURATION = 1.5; // 1.5 seconds smooth transition
      const currentRealTime = Date.now() / 1000;
      
      if (!initialCameraRef.current) {
        initialCameraRef.current = {
          center: map.getCenter(),
          zoom: map.getZoom(),
          pitch: map.getPitch(),
          bearing: map.getBearing(),
          timestamp: currentRealTime
        };
      }
      
      const tElapsed = currentRealTime - initialCameraRef.current.timestamp;
      const t = Math.min(1, tElapsed / TRANSITION_DURATION);
      
      // smoothstep easing
      const ease = t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
      
      if (t < 1) {
        const init = initialCameraRef.current;
        const cZoom = init.zoom + (targetZoom - init.zoom) * ease;
        const cPitch = init.pitch + (targetPitch - init.pitch) * ease;
        
        let db = targetBearing - init.bearing;
        while (db > 180) db -= 360;
        while (db < -180) db += 360;
        const cBearing = init.bearing + db * ease;
        
        const cLng = init.center.lng + (targetCenter[0] - init.center.lng) * ease;
        const cLat = init.center.lat + (targetCenter[1] - init.center.lat) * ease;
        
        map.jumpTo({
          center: [cLng, cLat],
          zoom: cZoom,
          pitch: cPitch,
          bearing: cBearing
        });
      } else {
        map.jumpTo({
          center: targetCenter,
          bearing: targetBearing,
          pitch: targetPitch,
          zoom: targetZoom
        });
      }
    } else {
      initialCameraRef.current = null;
    }

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

  useEffect(() => {
    if (mapRef.current && routeInitializedRef.current) {
      updateRouteProgress(mapRef.current, cities, animationProgress, totalDistRef.current, legDistancesRef.current);
      if ((window as any)._updateSvgOverlay) {
        (window as any)._updateSvgOverlay();
      }
    }
  }, [animationProgress, cities]);

  return (
    <div className="w-full h-full relative" ref={containerRef}>
            
      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor="#CCFF00" />
          </linearGradient>
        </defs>
        <path d={fullSvgPath} fill="none" stroke={animationProgress === 0 ? routeColor : 'rgba(255, 255, 255, 0.3)'} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
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
            borderRadius: '8px',
            padding: '4px 8px',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            boxShadow: '0 4px 12px rgba(0,0,0,0.5)',
            transform: 'translateY(-30px)',
            lineHeight: 1,
          }}>
             <span style={{ color: '#fff', fontSize: '13px', fontWeight: 700, fontFamily: 'sans-serif', marginBottom: '2px' }}>{distanceBadge.text}</span>
             <span style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif' }}>{distanceBadge.text2}</span>
          </div>
        </div>
      )}
      
      {showElevation && elevationProfile && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 24, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'elevation' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('elevation')}
          onMouseDown={() => setActiveWindow && setActiveWindow('elevation')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }} className="pointer-events-none">
            <div>
              <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: '0 0 4px 0', fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Elevation Profile</h3>
              <div style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif', display: 'flex', alignItems: 'center', gap: '6px' }}>
                <span>{(totalDistRef.current / 1000).toFixed(0)} KM</span>
                <span style={{ color: '#4b5563' }}>•</span>
                <span>{Math.floor(durationSeconds / 60)}M {durationSeconds % 60}S</span>
              </div>
            </div>
            <button style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer', padding: '4px' }}>
              <GripHorizontal size={14} />
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
            {(() => {
              if (!elevationProfile || elevationProfile.length === 0) return null;
              const max = Math.max(...elevationProfile);
              const min = Math.min(...elevationProfile);
              const range = max - min || 1;
              
              const exactIdx = animationProgress * (elevationProfile.length - 1);
              const i1 = Math.floor(exactIdx);
              const i2 = Math.min(Math.ceil(exactIdx), elevationProfile.length - 1);
              const frac = exactIdx - i1;
              const currentElev = elevationProfile[i1] + frac * (elevationProfile[i2] - elevationProfile[i1]);
              
              const leftPct = animationProgress * 100;
              const bottomPct = ((currentElev - min) / range) * 100;
              
              return (
                <>
                  <div style={{
                    position: 'absolute', left: `${leftPct}%`, bottom: `${bottomPct}%`,
                    transform: 'translate(-50%, 50%)',
                    width: '6px', height: '6px', backgroundColor: '#CCFF00', borderRadius: '50%', border: '1px solid black', zIndex: 21, pointerEvents: 'none', transition: 'none'
                  }} />
                  <div style={{ 
                    position: 'absolute', left: `${leftPct}%`, bottom: `${bottomPct}%`, 
                    transform: 'translate(-50%, -12px)',
                    color: '#fff', fontSize: '9px', fontWeight: 700, fontFamily: 'sans-serif', 
                    background: 'rgba(0,0,0,0.8)', padding: '2px 4px', borderRadius: '4px',
                    zIndex: 20, pointerEvents: 'none', transition: 'none'
                  }}>
                    {Math.round(currentElev)}m
                  </div>
                </>
              );
            })()}
            
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
        </Rnd>
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
