'use client';

import React from 'react';
import type { EditorState } from '@/hooks/useEditorState';

interface CameraPanelProps {
  cameraMode: 'static' | 'follow' | 'orbit';
  onChange: <K extends keyof EditorState>(key: K, value: EditorState[K]) => void;
}

export default function CameraPanel({ cameraMode, onChange }: CameraPanelProps) {
  return (
    <div className="p-4">
      <h3 className="text-[10px] font-bold text-white uppercase tracking-widest mb-3">
        Camera
      </h3>
      <div className="flex gap-2">
        {[
          { label: 'Static', value: 'static' },
          { label: 'Follow', value: 'follow' },
          { label: 'Orbit', value: 'orbit' },
        ].map(({ label, value }) => (
          <button
            key={value}
            onClick={() => onChange('cameraMode', value as any)}
            className={`flex-1 py-1.5 rounded text-[11px] font-medium transition-colors ${
              cameraMode === value
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
