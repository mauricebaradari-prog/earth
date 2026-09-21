'use client';

import sparklinesData from '../data/sparklines.json';
import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { 
  Play, Pause, RotateCcw, 
  Map as MapIcon, Plane, Car, Palette, MapPin, Settings, Download, Camera, Check, Search, Gauge, Mountain
} from 'lucide-react';
import { Video } from 'lucide-react';
import { useEditorState } from '@/hooks/useEditorState';
// import GlobeMap from '@/components/GlobeMap';
import AnimationsPanel from '@/components/panels/AnimationsPanel';
import CameraPanel from '@/components/panels/CameraPanel';

const YouTubeOverlay = dynamic(() => import('@/components/YouTubeOverlay'), { ssr: false });
const GlobeMap = dynamic(() => import('@/components/GlobeMap'), { ssr: false });
function MiniElevationProfile({ routeId, active }: { routeId: string, active: boolean }) {
  const elevations = (sparklinesData as any)[routeId] || Array(20).fill(0);
  
  // Find min and max for scaling
  let min = Math.min(...elevations);
  let max = Math.max(...elevations);
  if (max === min) {
    max = min + 10;
  }
  const range = max - min;
  
  const points = [];
  const segments = elevations.length - 1;
  
  for (let i = 0; i <= segments; i++) {
    const norm = (elevations[i] - min) / range; // 0 to 1
    // scale to SVG height (0 to 16px, leaving padding)
    points.push(`${i * (40 / segments)},${18 - norm * 14}`);
  }
  
  const d = `M 0,20 L ${points.join(' L ')} L 40,20 Z`;
  const strokeColor = active ? 'rgba(0,0,0,0.5)' : 'rgba(204,255,0,0.6)';
  const fillColor = active ? 'rgba(0,0,0,0.1)' : 'rgba(204,255,0,0.1)';
  
  return (
    <svg width="40" height="20" viewBox="0 0 40 20" className="opacity-90">
      <path d={d} fill={fillColor} />
      <path d={`M ${points.join(' L ')}`} fill="none" stroke={strokeColor} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function Home() {
  const [openModal, setOpenModal] = useState<'none' | 'route' | 'speed' | 'camera'>('none');
  const [initialVideoPos, setInitialVideoPos] = useState<{ x: number; y: number } | null>(null);
  const [showElevation, setShowElevation] = useState(true);
  const [showVelocity, setShowVelocity] = useState(false);
  const [useGpsTrace, setUseGpsTrace] = useState(false);

  const {
    state,
    setMapStyle,
    set,
    setActiveRoute,
    setActiveWindow,
    startAnimation,
    stopAnimation,
    resetAnimation,
  } = useEditorState();

  const canAnimate = state.cities.length >= 2;

  function handlePlayRoute(routeId: string) {
    if (routeId !== state.activeRouteId) {
      setActiveRoute(routeId);
      // Wait for route to load, then start animation
      setTimeout(() => startAnimation(), 300);
    } else {
      if (state.animationProgress >= 1) {
        resetAnimation();
        setTimeout(startAnimation, 50);
      } else {
        startAnimation();
      }
    }
  }

  function handleStopRoute() {
    stopAnimation();
  }

  function handlePlayPause() {
    if (state.isAnimating) {
      stopAnimation();
    } else if (state.animationProgress >= 1) {
      resetAnimation();
      setTimeout(startAnimation, 50);
    } else {
      startAnimation();
    }
  }

  function handleSeek(progress: number) {
    set('animationProgress', progress);
    if ((window as any).__YT_PLAYER) {
      (window as any).__IS_SCRUBBING = true;
      (window as any).__YT_PLAYER.seekTo(progress * (state.durationSeconds || 2056), true);
      setTimeout(() => { (window as any).__IS_SCRUBBING = false; }, 500);
    }
  }

  return (
    <div className="h-screen w-full relative overflow-hidden bg-black text-white font-sans">
      
      {/* ── Map area ── */}
      <main className="absolute inset-0">
        <YouTubeOverlay 
          state={state} 
          startAnimation={startAnimation} 
          stopAnimation={stopAnimation} 
          initialPos={initialVideoPos} 
          setActiveWindow={setActiveWindow}
        />
        
        <GlobeMap
          cities={state.cities}
          routes={state.routes}
          vehicle={state.vehicle}
          mapStyle={state.mapStyle}
          globeAtmosphere={state.globeAtmosphere}
          animationProgress={state.animationProgress}
          isAnimating={state.isAnimating}
          cameraMode={state.cameraMode}
          routeColor={state.routeColor}
          routeWidth={state.routeWidth}
          showElevation={showElevation}
          showVelocity={showVelocity}
          durationSeconds={state.durationSeconds}
          onSeek={handleSeek}
          activeWindow={state.activeWindow}
          setActiveWindow={setActiveWindow}
          onPlayRoute={handlePlayRoute}
          onStopRoute={handleStopRoute}
          onPoint1Projected={(x: number, y: number) => {
            if (typeof window === 'undefined') return;
            const videoWidth = 320;
            const videoHeight = 204;
            const padding = 20;
            
            // Calculate ideal position
            let idealX = x - 180;
            let idealY = y + 30;
            
            // Clamp X
            const maxX = window.innerWidth - videoWidth - padding;
            idealX = Math.max(padding, Math.min(idealX, maxX));
            
            // Clamp Y
            const maxY = window.innerHeight - videoHeight - padding;
            idealY = Math.max(padding, Math.min(idealY, maxY));
            
            setInitialVideoPos({ x: idealX, y: idealY });
          }}
        />

        {/* Animation progress bar overlay */}
        {(state.isAnimating || state.animationProgress > 0) && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-black/40 z-50">
            <div
              className="h-full transition-all duration-100"
              style={{ width: `${state.animationProgress * 100}%`, background: 'linear-gradient(to right, #FFFFFF, #CCFF00)' }}
            />
          </div>
        )}
      </main>



      {/* ── Left Gradient Backdrop ── */}
      <div className="absolute top-0 left-0 bottom-0 w-64 bg-gradient-to-r from-black/80 via-black/40 to-transparent z-40 pointer-events-none" />

      {/* ── Floating Minimalist UI (Top Left) ── */}
      <div className="absolute top-6 left-6 z-50 flex flex-col items-center gap-4">
        
        {/* Logo */}
        <div className="mb-2 pointer-events-none">
          <img src="/logo.svg" alt="Logo" className="h-14 invert opacity-90 drop-shadow-md" />
        </div>

        {/* Play Button */}
        <button
          id="top-left-play-btn"
          onClick={handlePlayPause}
          disabled={!canAnimate}
          className={`w-14 h-14 rounded-full flex items-center justify-center shadow-2xl backdrop-blur-md transition-all border ${
            canAnimate
              ? state.isAnimating
                ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50 hover:bg-lime-400/30'
                : 'bg-black/60 text-white border-white/20 hover:bg-black/80 hover:border-white/40'
              : 'bg-gray-800 text-gray-600 border-gray-700 cursor-not-allowed'
          }`}
        >
          {state.isAnimating ? <Pause size={24} fill="currentColor" /> : <Play size={24} fill="currentColor" className="ml-1" />}
        </button>

        {/* Floating Modals Container */}
        <div className="relative">
          
          {/* Action Buttons Row */}
          <div className="flex flex-col gap-2">
            <button
              onClick={() => setOpenModal(openModal === 'route' ? 'none' : 'route')}
              className={`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border ${
                openModal === 'route' 
                  ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }`}
              title="Switch Route"
            >
              <MapPin size={18} />
            </button>


            
            
            
            <button
              onClick={() => setOpenModal(openModal === 'speed' ? 'none' : 'speed')}
              className={`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border ${
                openModal === 'speed' 
                  ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }`}
              title="Animation Speed"
            >
              <Gauge size={18} />
            </button>
            <button
              onClick={() => setOpenModal(openModal === 'camera' ? 'none' : 'camera')}
              className={`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border ${
                openModal === 'camera' 
                  ? 'bg-[#CCFF00]/20 text-[#CCFF00] border-[#CCFF00]/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }`}
              title="Camera Behavior"
            >
              <Video size={18} />
            </button>

            {(state.isAnimating || state.animationProgress > 0) && (
              <button
                onClick={resetAnimation}
                className="w-10 h-10 rounded-full flex items-center justify-center bg-black/50 text-gray-400 border border-white/10 hover:bg-black/70 hover:text-white transition-all mt-2"
                title="Reset animation"
              >
                <RotateCcw size={16} />
              </button>
            )}
          </div>

          {/* Floating Panels */}
          {openModal !== 'none' && (
            <div 
              className="absolute left-14 w-72 bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden transition-all duration-200"
              style={{
                top: openModal === 'speed' ? 48 : openModal === 'camera' ? 96 : 0
              }}
            >
              
              
              {openModal === 'route' && (
                <div className="p-4 flex flex-col gap-2">
                  <h3 className="text-[10px] font-bold text-white uppercase tracking-widest mb-3">Switch Route</h3>
                  {state.routes.map(r => (
                    <button
                      key={r.id}
                      onClick={() => {
                        setActiveRoute(r.id);
                        setOpenModal('none');
                      }}
                      className={`text-left px-3 py-2 text-sm rounded-lg transition-colors w-full flex justify-between items-center ${
                        state.activeRouteId === r.id 
                          ? 'bg-[#CCFF00] text-black font-medium border border-transparent' 
                          : 'bg-white/5 text-white/70 border border-transparent hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <span>{r.name}</span>
                      <MiniElevationProfile routeId={r.id} active={state.activeRouteId === r.id} />
                    </button>
                  ))}
                </div>
              )}
              {openModal === 'speed' && (
                <AnimationsPanel
                  animSpeed={state.animSpeed}
                  cameraMode={state.cameraMode}
                  onChange={set}
                />
              )}
              {openModal === 'camera' && (
                <CameraPanel
                  cameraMode={state.cameraMode}
                  onChange={set}
                />
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
