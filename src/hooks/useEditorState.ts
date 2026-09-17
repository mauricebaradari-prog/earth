import { useState, useCallback, useRef, useEffect } from 'react';

export interface City {
  id: string;
  name: string;
  country: string;
  lat: number;
  lng: number;
}

export type VehicleType = 'plane' | 'car' | 'boat' | 'walk';
export type MapStyleId = 'satellite' | 'streets' | 'terrain';

export interface VehicleConfig {
  type: VehicleType;
  color: string;
  size: number; // 1-3
}

export interface RouteConfig {
  id: string;
  name: string;
  cities: City[];
  videoId: string;
  durationSeconds: number;
  routeColor: string;
}

export interface EditorState {
  routes: RouteConfig[];
  activeRouteId: string;
  // Derived from active route for backward compat
  cities: City[];
  vehicle: VehicleConfig;
  mapStyle: MapStyleId;
  animSpeed: number; // 0.5 – 4
  cameraMode: 'static' | 'follow' | 'orbit';
  durationSeconds: number;
  isAnimating: boolean;
  animationProgress: number; // 0-1 global across all legs
  globeAtmosphere: boolean;
  routeColor: string;
  routeWidth: number;
  videoId: string;
}

export const ROUTES: RouteConfig[] = [
  {
    id: 'route-1',
    name: 'Agios Georgios → Polis',
    cities: [
      { id: '2', name: 'Agios Georgios', country: 'Cyprus', lat: 34.8838031, lng: 32.3446892 },
      { id: '3', name: 'Pano Arodes', country: 'Cyprus', lat: 34.9244925, lng: 32.4196612 },
      { id: '4', name: 'Ineia', country: 'Cyprus', lat: 34.963983, lng: 32.3824113 },
      { id: '5', name: 'Androlikou', country: 'Cyprus', lat: 34.9882794, lng: 32.3788797 },
      { id: '6', name: 'Polis', country: 'Cyprus', lat: 35.0246073, lng: 32.4127148 },
    ],
    videoId: '5EgtgRoC8NI',
    durationSeconds: 34 * 60 + 16, // 34:16
    routeColor: '#CCFF00',
  },
  {
    id: 'route-2',
    name: 'Polis → Pomos',
    cities: [
      { id: 'r2-1', name: 'Polis Chrysochous', country: 'Cyprus', lat: 35.0393148, lng: 32.4042644 },
      { id: 'r2-2', name: 'Polis East', country: 'Cyprus', lat: 35.041072, lng: 32.4174365 },
      { id: 'r2-3', name: 'Polis Outskirts', country: 'Cyprus', lat: 35.0394087, lng: 32.4246033 },
      { id: 'r2-4', name: 'Chrysochous Valley', country: 'Cyprus', lat: 35.0378529, lng: 32.4335303 },
      { id: 'r2-5', name: 'Chrysochous Bay', country: 'Cyprus', lat: 35.0630401, lng: 32.4641189 },
      { id: 'r2-6', name: 'Agia Marina', country: 'Cyprus', lat: 35.127973, lng: 32.5163844 },
      { id: 'r2-7', name: 'Pomos', country: 'Cyprus', lat: 35.151795, lng: 32.5391915 },
    ],
    videoId: 'xBqcc3zJVBU',
    durationSeconds: 31 * 60 + 25, // 31:25
    routeColor: '#CCFF00',
  },
];

function getActiveRoute(routes: RouteConfig[], activeId: string): RouteConfig {
  return routes.find(r => r.id === activeId) || routes[0];
}

export function useEditorState() {
  const [state, setState] = useState<EditorState>(() => {
    const active = ROUTES[0];
    return {
      routes: ROUTES,
      activeRouteId: active.id,
      cities: active.cities,
      vehicle: { type: 'plane', color: '#CCFF00', size: 2 },
      mapStyle: 'satellite',
      animSpeed: 1,
    cameraMode: 'orbit',
      durationSeconds: active.durationSeconds,
      isAnimating: false,
      animationProgress: 0,
      globeAtmosphere: true,
      routeColor: active.routeColor,
      routeWidth: 2,
      videoId: active.videoId,
    };
  });

  const rafRef = useRef<number | null>(null);
  const lastTimeRef = useRef<number | null>(null);

  const setMapStyle = useCallback((s: MapStyleId) => {
    setState((prev) => ({ ...prev, mapStyle: s }));
  }, []);

  const set = useCallback(<K extends keyof EditorState>(key: K, value: EditorState[K]) => {
    setState((prev) => ({ ...prev, [key]: value }));
  }, []);

  const setActiveRoute = useCallback((routeId: string) => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    setState((prev) => {
      const route = getActiveRoute(prev.routes, routeId);
      return {
        ...prev,
        activeRouteId: routeId,
        cities: route.cities,
        durationSeconds: route.durationSeconds,
        routeColor: route.routeColor,
        videoId: route.videoId,
        isAnimating: false,
        animationProgress: 0,
      };
    });
  }, []);

  // Animation loop
  const startAnimation = useCallback(() => {
    setState((prev) => {
      const progress = prev.animationProgress >= 1 ? 0 : prev.animationProgress;
      return { ...prev, isAnimating: true, animationProgress: progress };
    });
    lastTimeRef.current = null;

    const tick = (now: number) => {
      if (lastTimeRef.current === null) lastTimeRef.current = now;
      const dt = (now - lastTimeRef.current) / 1000;
      lastTimeRef.current = now;

      setState((prev) => {
        if (!prev.isAnimating) return prev;
        const speed = prev.animSpeed / (prev.durationSeconds || 2056); // progress units per second
        const next = prev.animationProgress + dt * speed;
        if (next >= 1) {
          return { ...prev, animationProgress: 1, isAnimating: false };
        }
        return { ...prev, animationProgress: next };
      });

      rafRef.current = requestAnimationFrame(tick);
    };

    rafRef.current = requestAnimationFrame(tick);
  }, []);

  const stopAnimation = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    setState((prev) => ({ ...prev, isAnimating: false }));
  }, []);

  const resetAnimation = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    setState((prev) => ({ ...prev, isAnimating: false, animationProgress: 0 }));
  }, []);

  useEffect(() => {
    return () => {
      if (rafRef.current) cancelAnimationFrame(rafRef.current);
    };
  }, []);

  return {
    state,
    setMapStyle,
    set,
    setActiveRoute,
    startAnimation,
    stopAnimation,
    resetAnimation,
  };
}
