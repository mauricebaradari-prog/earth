import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# Add import at the top
if "import sparklinesData from '../data/sparklines.json';" not in content:
    content = content.replace("import { useState", "import sparklinesData from '../data/sparklines.json';\nimport { useState")

# Replace MiniElevationProfile component
old_comp = """function MiniElevationProfile({ seed, active }: { seed: string, active: boolean }) {
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
}"""

new_comp = """function MiniElevationProfile({ routeId, active }: { routeId: string, active: boolean }) {
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
}"""

content = content.replace(old_comp, new_comp)

old_jsx = "<MiniElevationProfile seed={r.id + r.name} active={state.activeRouteId === r.id} />"
new_jsx = "<MiniElevationProfile routeId={r.id} active={state.activeRouteId === r.id} />"

content = content.replace(old_jsx, new_jsx)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
