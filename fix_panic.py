import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Add Rnd import
if "import { Rnd }" not in content:
    content = content.replace("import * as maplibregl from 'maplibre-gl';", "import * as maplibregl from 'maplibre-gl';\nimport { Rnd } from 'react-rnd';")

# 2. Restore globeAtmosphere safely
fog_patch = """      map.once('style.load', () => {
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
"""
content = content.replace("""      map.once('style.load', () => {
        (map as any).setProjection({ type: 'globe' });""", fog_patch)

# 3. Replace the fake elevation profile UI with the awesome draggable one!
elev_regex = r"      \{showElevation && elevationProfile && \(\n        <div style=\{\{ position: 'absolute'.*?\n      \}\)"
awesome_elev = """      {/* ── Elevation Profile Chart ── */}
      {showElevation && elevationProfile && elevationProfile.length > 0 && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 424 : 0, y: 24, width: 400, height: 140 }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
        >
          <div className="w-full h-full bg-black/60 backdrop-blur-md p-4 rounded-xl border border-white/10 shadow-2xl flex flex-col gap-2 cursor-grab active:cursor-grabbing">
            <div className="text-white text-xs font-bold tracking-wide uppercase opacity-80 flex justify-between pointer-events-none">
              <span>Elevation Profile</span>
            </div>
            <div className="relative w-full flex-1 mt-1 pointer-events-auto cursor-pointer" onClick={(e) => {
                if (!onSeek) return;
                const rect = e.currentTarget.getBoundingClientRect();
                let p = (e.clientX - rect.left) / rect.width;
                p = Math.max(0, Math.min(1, p));
                onSeek(p);
            }}>
              <svg width="100%" height="100%" viewBox="0 0 368 70" preserveAspectRatio="none">
                {(() => {
                  const min = Math.min(...elevationProfile);
                  const max = Math.max(...elevationProfile);
                  const diff = max - min || 1;
                  const pts = elevationProfile.map((elv, i) => {
                    const x = (i / (elevationProfile.length - 1)) * 368;
                    const y = 70 - ((elv - min) / diff) * 60; // leave 10px padding at top
                    return `${x},${y}`;
                  });
                  const pathData = `M 0,70 L ${pts.join(' L ')} L 368,70 Z`;
                  const lineData = `M ${pts.join(' L ')}`;
                  
                  // Calculate moving dot
                  const dotX = animationProgress * 368;
                  const exactIdx = animationProgress * (elevationProfile.length - 1);
                  const idx1 = Math.floor(exactIdx);
                  const idx2 = Math.min(elevationProfile.length - 1, idx1 + 1);
                  const frac = exactIdx - idx1;
                  const elv = elevationProfile[idx1] + (elevationProfile[idx2] - elevationProfile[idx1]) * frac;
                  const dotY = 70 - ((elv - min) / diff) * 60;
                  
                  // Adjust text anchor so it doesn't clip
                  let anchor = "middle";
                  let offsetX = 0;
                  if (dotX < 20) { anchor = "start"; offsetX = 8; }
                  else if (dotX > 348) { anchor = "end"; offsetX = -8; }
                  
                  return (
                    <>
                      <defs>
                        <linearGradient id="elevGrad" x1="0" y1="0" x2="0" y2="1">
                          <stop offset="0%" stopColor={routeColor} stopOpacity={0.6} />
                          <stop offset="100%" stopColor={routeColor} stopOpacity={0.0} />
                        </linearGradient>
                      </defs>
                      <path d={pathData} fill="url(#elevGrad)" className="pointer-events-none" />
                      <path d={lineData} fill="none" stroke={routeColor} strokeWidth="2" strokeLinejoin="round" className="pointer-events-none" />
                      
                      {/* Moving Dot */}
                      <circle cx={dotX} cy={dotY} r="4" fill="white" stroke="#111" strokeWidth="2" className="pointer-events-none" />
                      <line x1={dotX} y1={dotY} x2={dotX} y2="70" stroke="white" strokeWidth="1" strokeDasharray="2 2" strokeOpacity={0.5} className="pointer-events-none" />
                      
                      {/* Following Text */}
                      <text x={dotX + offsetX} y={Math.max(12, dotY - 10)} fill="white" fontSize="12" fontWeight="bold" textAnchor={anchor as any} filter="drop-shadow(0px 1px 2px rgba(0,0,0,0.8))" className="pointer-events-none">
                        {Math.round(elv)}m
                      </text>
                    </>
                  );
                })()}
              </svg>
            </div>
          </div>
        </Rnd>
      )"""

content = re.sub(elev_regex, awesome_elev, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
