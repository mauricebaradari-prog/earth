import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

sparkline_comp = """function MiniElevationProfile({ seed, active }: { seed: string, active: boolean }) {
  // Deterministic pseudo-random based on string seed
  const hash = seed.split('').reduce((a, b) => { a = ((a << 5) - a) + b.charCodeAt(0); return a & a }, 0);
  
  const points = [];
  const segments = 12;
  let val = 30 + (Math.abs(hash) % 20);
  
  for (let i = 0; i <= segments; i++) {
    points.push(`${i * (40 / segments)},${20 - (val / 100) * 16}`);
    const noise = (Math.abs(hash * (i + 1)) % 40) - 20;
    val = Math.max(10, Math.min(90, val + noise));
  }
  
  const d = `M 0,20 L ${points.join(' L ')} L 40,20 Z`;
  const strokeColor = active ? 'rgba(0,0,0,0.4)' : 'rgba(204,255,0,0.5)';
  const fillColor = active ? 'rgba(0,0,0,0.1)' : 'rgba(204,255,0,0.1)';
  
  return (
    <svg width="40" height="20" viewBox="0 0 40 20" className="opacity-80">
      <path d={d} fill={fillColor} />
      <path d={`M ${points.join(' L ')}`} fill="none" stroke={strokeColor} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}

export default function Home() {"""

content = content.replace("export default function Home() {", sparkline_comp)

old_btn = """                      className={`text-left px-3 py-2 text-sm rounded-lg transition-colors ${
                        state.activeRouteId === r.id 
                          ? 'bg-[#CCFF00] text-black font-medium border border-transparent' 
                          : 'bg-white/5 text-white/70 border border-transparent hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      {r.name}
                    </button>"""

new_btn = """                      className={`text-left px-3 py-2 text-sm rounded-lg transition-colors w-full flex justify-between items-center ${
                        state.activeRouteId === r.id 
                          ? 'bg-[#CCFF00] text-black font-medium border border-transparent' 
                          : 'bg-white/5 text-white/70 border border-transparent hover:bg-white/10 hover:text-white'
                      }`}
                    >
                      <span>{r.name}</span>
                      <MiniElevationProfile seed={r.id + r.name} active={state.activeRouteId === r.id} />
                    </button>"""

content = content.replace(old_btn, new_btn)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
