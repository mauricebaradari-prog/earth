import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Add showVelocity prop
content = re.sub(
    r'showElevation\?: boolean;',
    r'showElevation?: boolean;\n  showVelocity?: boolean;',
    content
)

content = re.sub(
    r'showElevation,',
    r'showElevation,\n  showVelocity,',
    content
)

# Add Gauge icon to imports
content = re.sub(
    r'import \{ Play, Pause, Square, Map as MapIcon, Route, Compass, Mountain \} from \'lucide-react\';',
    r"import { Play, Pause, Square, Map as MapIcon, Route, Compass, Mountain, Gauge } from 'lucide-react';",
    content
)

# Add ref for velocity text
content = re.sub(
    r'const vehicleDotRef = React\.useRef<HTMLDivElement>\(null\);',
    r"const velocityTextRef = React.useRef<HTMLSpanElement>(null);\n  const vehicleDotRef = React.useRef<HTMLDivElement>(null);",
    content
)

# Add Haversine distance function outside component
haversine = """
function getDistanceKm(lat1: number, lon1: number, lat2: number, lon2: number) {
  const R = 6371; // Radius of the earth in km
  const dLat = (lat2 - lat1) * Math.PI / 180;  
  const dLon = (lon2 - lon1) * Math.PI / 180; 
  const a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(lat1 * Math.PI / 180) * Math.cos(lat2 * Math.PI / 180) * 
    Math.sin(dLon/2) * Math.sin(dLon/2); 
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  return R * c;
}

export default function GlobeMap({
"""
content = content.replace("export default function GlobeMap({", haversine)

# Update _updateSvgOverlay to calculate velocity
old_time_calc = """             const distKm = displayDist.toFixed(0);
             const m = Math.floor(displaySecs / 60);
             const s = Math.floor(displaySecs % 60);"""

new_time_calc = """             const distKm = displayDist.toFixed(0);
             const m = Math.floor(displaySecs / 60);
             const s = Math.floor(displaySecs % 60);

             if (velocityTextRef.current) {
                const segDistKm = getDistanceKm(p1[1], p1[0], p2[1], p2[0]);
                const timeSecs = currentDuration / Math.max(1, fullPts.length - 1);
                let speedKmh = (segDistKm / timeSecs) * 3600;
                
                // Extremely simple low-pass filter for smooth velocity numbers
                if (!(window as any)._smoothSpeed || Math.abs((window as any)._smoothSpeed - speedKmh) > 50) {
                    (window as any)._smoothSpeed = speedKmh;
                } else {
                    (window as any)._smoothSpeed = (window as any)._smoothSpeed * 0.95 + speedKmh * 0.05;
                }
                
                velocityTextRef.current.textContent = `${Math.round((window as any)._smoothSpeed)}`;
             }"""

content = content.replace(old_time_calc, new_time_calc)

# Reset speed to 0 when not animating
old_else = """          } else {
             if (vehicleDotRef.current) vehicleDotRef.current.style.display = 'none';"""

new_else = """          } else {
             if (velocityTextRef.current) velocityTextRef.current.textContent = "0";
             if (vehicleDotRef.current) vehicleDotRef.current.style.display = 'none';"""

content = content.replace(old_else, new_else)

# Add Velocity panel JSX
velocity_jsx = """
      {showVelocity && (
        <Rnd
          default={{ x: 24, y: 24, width: 220, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: 60 }}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing flex flex-col items-center justify-center">
          <div className="flex items-center gap-2 mb-2 w-full pointer-events-none">
            <Gauge size={14} className="text-[#CCFF00]" />
            <h3 style={{ margin: 0, color: '#fff', fontSize: '11px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>Velocity</h3>
          </div>
          <div className="flex items-baseline gap-1 mt-2">
            <span ref={velocityTextRef} className="text-4xl font-mono font-bold text-white tracking-tighter">0</span>
            <span className="text-[#CCFF00] font-bold text-sm">km/h</span>
          </div>
        </div>
        </Rnd>
      )}"""

# Insert right after the distanceBadge block
content = re.sub(
    r'(<div className="w-px h-3 bg-white/20" />\s*<span ref=\{distanceTimeRef\} className="text-gray-300"></span>\s*</div>\s*</div>)',
    r'\1' + velocity_jsx,
    content
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
