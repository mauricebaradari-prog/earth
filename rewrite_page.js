const fs = require('fs');

const code = `
'use client';

import React, { useState } from 'react';
import dynamic from 'next/dynamic';
import { Play, Pause, RotateCcw, Palette, Gauge } from 'lucide-react';
import { useEditorState } from '@/hooks/useEditorState';
import StylePanel from '@/components/panels/StylePanel';
import AnimationsPanel from '@/components/panels/AnimationsPanel';
import GlobeMap from '@/components/GlobeMap';

const YouTubeOverlay = dynamic(() => import('@/components/YouTubeOverlay'), { ssr: false });

export default function Home() {
  const [openModal, setOpenModal] = useState<'none' | 'style' | 'speed'>('none');

  const {
    state,
    setMapStyle,
    set,
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

  return (
    <div className="h-screen w-full relative overflow-hidden bg-black text-white font-sans">
      
      {/* ── Map area ── */}
      <main className="absolute inset-0">
        <YouTubeOverlay state={state} startAnimation={startAnimation} stopAnimation={stopAnimation} />
        
        <GlobeMap
          cities={state.cities}
          mapStyle={state.mapStyle}
          animationProgress={state.animationProgress}
          isAnimating={state.isAnimating}
          routeColor={state.routeColor}
          routeWidth={state.routeWidth}
        />

        {/* Animation progress bar overlay */}
        {(state.isAnimating || state.animationProgress > 0) && (
          <div className="absolute bottom-0 left-0 right-0 h-1 bg-black/40 z-50">
            <div
              className="h-full bg-gradient-to-r from-yellow-400 to-orange-500 transition-all duration-100"
              style={{ width: \`\${state.animationProgress * 100}%\` }}
            />
          </div>
        )}
      </main>

      {/* ── Floating Minimalist UI (Top Left) ── */}
      <div className="absolute top-6 left-6 z-50 flex flex-col gap-4">
        
        {/* Play Button */}
        <button
          id="top-left-play-btn"
          onClick={handlePlayPause}
          disabled={!canAnimate}
          className={\`w-14 h-14 rounded-full flex items-center justify-center shadow-2xl backdrop-blur-md transition-all border \${
            canAnimate
              ? state.isAnimating
                ? 'bg-yellow-400/20 text-yellow-400 border-yellow-400/50 hover:bg-yellow-400/30'
                : 'bg-black/60 text-white border-white/20 hover:bg-black/80 hover:border-white/40'
              : 'bg-gray-800 text-gray-600 border-gray-700 cursor-not-allowed'
          }\`}
        >
          {state.isAnimating ? <Pause size={24} fill="currentColor" /> : <Play size={24} fill="currentColor" className="ml-1" />}
        </button>

        {/* Floating Modals Container */}
        <div className="relative">
          
          {/* Action Buttons Row */}
          <div className="flex flex-col gap-2">
            <button
              onClick={() => setOpenModal(openModal === 'style' ? 'none' : 'style')}
              className={\`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border \${
                openModal === 'style' 
                  ? 'bg-yellow-400/20 text-yellow-400 border-yellow-400/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }\`}
              title="Map Style"
            >
              <Palette size={18} />
            </button>
            
            <button
              onClick={() => setOpenModal(openModal === 'speed' ? 'none' : 'speed')}
              className={\`w-10 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border \${
                openModal === 'speed' 
                  ? 'bg-yellow-400/20 text-yellow-400 border-yellow-400/50' 
                  : 'bg-black/50 text-white border-white/10 hover:bg-black/70'
              }\`}
              title="Animation Speed"
            >
              <Gauge size={18} />
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
            <div className="absolute top-0 left-14 w-72 bg-black/80 backdrop-blur-xl border border-white/10 rounded-2xl shadow-2xl overflow-hidden">
              {openModal === 'style' && (
                <StylePanel
                  mapStyle={state.mapStyle}
                  routeColor={state.routeColor}
                  routeWidth={state.routeWidth}
                  onMapStyle={setMapStyle}
                  onRouteColor={(c) => set('routeColor', c)}
                  onRouteWidth={(w) => set('routeWidth', w)}
                />
              )}
              {openModal === 'speed' && (
                <AnimationsPanel
                  animSpeed={state.animSpeed}
                  onChange={set}
                  cameraMode="follow"
                />
              )}
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
\`;

fs.writeFileSync('src/app/page.tsx', code);
