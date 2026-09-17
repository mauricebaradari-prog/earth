'use client';

import React from 'react';
import type { MapStyleId } from '@/hooks/useEditorState';

interface MapPanelProps {
  mapStyle: MapStyleId;
  onMapStyle: (s: MapStyleId) => void;
}

export default function MapPanel({ mapStyle, onMapStyle }: MapPanelProps) {
  return (
    <div className="p-4">
      <h3 className="text-[10px] font-bold text-white uppercase tracking-widest mb-3">
        Map Style
      </h3>
      <div className="flex gap-2">
        {[
          { label: 'Satellite', value: 'satellite' },
          { label: 'Streets', value: 'streets' },
          { label: 'Terrain', value: 'terrain' },
        ].map(({ label, value }) => (
          <button
            key={value}
            onClick={() => onMapStyle(value as MapStyleId)}
            className={`flex-1 py-1.5 rounded text-[11px] font-medium transition-colors ${
              mapStyle === value
                ? 'bg-[#CCFF00] text-black'
                : 'bg-white/5 text-gray-400 hover:bg-white/10 hover:text-white'
            }`}
          >
            {label}
          </button>
        ))}
      </div>
    </div>
  );
}
