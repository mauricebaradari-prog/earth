'use client';

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { 
  Play, Pause, RotateCcw, 
  Map as MapIcon, Plane, Car, Palette, MapPin, Settings, Download, Camera, Check, Search, Gauge, Mountain
} from 'lucide-react';
import { Video } from 'lucide-react';
import { useEditorState } from '@/hooks/useEditorState';
import GlobeMap from '@/components/GlobeMap';
import AnimationsPanel from '@/components/panels/AnimationsPanel';
import CameraPanel from '@/components/panels/CameraPanel';

const YouTubeOverlay = dynamic(() => import('@/components/YouTubeOverlay'), { ssr: false });

export default function Home() {
  const [openModal, setOpenModal] = useState<'none' | 'route' | 'speed' | 'camera'>('none');
  const [initialVideoPos, setInitialVideoPos] = useState<{ x: number; y: number } | null>(null);
  const [showElevation, setShowElevation] = useState(true);

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
          durationSeconds={state.durationSeconds}
          onSeek={handleSeek}
          activeWindow={state.activeWindow}
          setActiveWindow={setActiveWindow}
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



      {/* ── Floating Minimalist UI (Top Left) ── */}
      <div className="absolute top-6 left-6 z-50 flex flex-col items-start gap-4">
        
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
                      className={`text-left px-3 py-2 text-sm rounded-lg transition-colors ${
                        state.activeRouteId === r.id 
                          ? 'bg-[#CCFF00] text-black font-medium border border-transparent' 
                          : 'bg-white/5 text-white/70 border border-transparent hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      {r.name}
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
