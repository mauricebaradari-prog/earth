import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Add velocityNeedleRef
if "velocityNeedleRef" not in content:
    content = content.replace(
        "const velocityTextRef = React.useRef<HTMLSpanElement>(null);",
        "const velocityTextRef = React.useRef<HTMLSpanElement>(null);\n  const velocityNeedleRef = React.useRef<SVGGElement>(null);"
    )

# Update DOM mutation to rotate the needle
old_mutation = """                velocityTextRef.current.textContent = `${Math.round((window as any)._smoothSpeed)}`;"""

new_mutation = """                const currentSpeed = (window as any)._smoothSpeed;
                velocityTextRef.current.textContent = `${Math.round(currentSpeed)}`;
                if (velocityNeedleRef.current) {
                    // Map 0 - 150 km/h to -90 to +90 degrees
                    const clampedSpeed = Math.max(0, Math.min(150, currentSpeed));
                    const angle = -90 + (clampedSpeed / 150) * 180;
                    velocityNeedleRef.current.style.transform = `rotate(${angle}deg)`;
                }"""
content = content.replace(old_mutation, new_mutation)

old_else = """             if (velocityTextRef.current) velocityTextRef.current.textContent = "0";"""
new_else = """             if (velocityTextRef.current) velocityTextRef.current.textContent = "0";
             if (velocityNeedleRef.current) velocityNeedleRef.current.style.transform = 'rotate(-90deg)';"""
content = content.replace(old_else, new_else)

# Replace Velocity panel JSX
old_panel = """      {showVelocity && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 200, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: 60 }}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing flex flex-col items-center justify-center">
          <div className="flex items-center gap-2 mb-2 w-full pointer-events-none text-white/50">
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

new_panel = """      {showVelocity && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 200, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'velocity' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('velocity')}
          onMouseDown={() => setActiveWindow && setActiveWindow('velocity')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }} className="pointer-events-none">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Gauge size={14} className="text-[#CCFF00]" />
              <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: 0, fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Velocity</h3>
            </div>
            <button style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer', padding: '4px' }}>
              <GripHorizontal size={14} />
            </button>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', position: 'relative', width: '100%', height: '120px' }} className="pointer-events-none">
            <svg width="220" height="120" viewBox="0 0 220 120" style={{ overflow: 'visible' }}>
              <defs>
                <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#ef4444" />
                  <stop offset="50%" stopColor="#eab308" />
                  <stop offset="100%" stopColor="#22c55e" />
                </linearGradient>
              </defs>
              <path d="M 20 100 A 90 90 0 0 1 200 100" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="12" strokeLinecap="round" />
              <path d="M 20 100 A 90 90 0 0 1 200 100" fill="none" stroke="url(#gaugeGrad)" strokeWidth="12" strokeLinecap="round" />
              
              <g ref={velocityNeedleRef} style={{ transformOrigin: '110px 100px', transform: 'rotate(-90deg)', willChange: 'transform', transition: 'transform 0.1s linear' }}>
                <polygon points="106,100 114,100 110,25" fill="#ffffff" />
                <circle cx="110" cy="100" r="6" fill="#111" stroke="#ffffff" strokeWidth="2" />
              </g>
              
              <text x="20" y="118" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="600" textAnchor="middle">0</text>
              <text x="110" y="20" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="600" textAnchor="middle">75</text>
              <text x="200" y="118" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="600" textAnchor="middle">150</text>
            </svg>
            <div style={{ position: 'absolute', bottom: '0px', width: '100%', textAlign: 'center' }}>
              <span ref={velocityTextRef} style={{ color: '#fff', fontSize: '32px', fontWeight: 800, fontFamily: 'monospace', letterSpacing: '-0.05em' }}>0</span>
              <span style={{ color: '#9ca3af', fontSize: '12px', fontWeight: 600, marginLeft: '4px' }}>km/h</span>
            </div>
          </div>
        </div>
        </Rnd>
      )}"""

content = content.replace(old_panel, new_panel)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
