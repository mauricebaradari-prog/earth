import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

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

# Find the end of the elevation profile panel and insert it there
content = re.sub(
    r'(</Rnd>\s*)\s*(\{\/\* ── Top Right Controls ── \*\/|\{/\* ── Camera Mode Toolbar)',
    r'\1' + velocity_jsx + r'\n      \2',
    content
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
