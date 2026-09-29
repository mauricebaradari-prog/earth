const fs = require('fs');

let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

const compassUI = `
      {showCompass && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 520, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'velocity' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('velocity')}
          onMouseDown={() => setActiveWindow && setActiveWindow('velocity')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }} className="pointer-events-none">
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <Compass size={14} className="text-[#CCFF00]" />
              <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: 0, fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Heading</h3>
            </div>
            <button style={{ background: 'none', border: 'none', color: '#9ca3af', cursor: 'pointer', padding: '4px' }}>
              <GripHorizontal size={14} />
            </button>
          </div>
          
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '170px' }} className="pointer-events-none">
            <svg width="220" height="130" viewBox="0 0 220 130" style={{ overflow: 'visible' }}>
              <circle cx="110" cy="65" r="55" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="8" />
              
              <text x="110" y="22" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">N</text>
              <text x="110" y="116" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">S</text>
              <text x="63" y="68" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">W</text>
              <text x="157" y="68" fill="#6b7280" fontSize="10" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">E</text>

              <g ref={compassNeedleRef} style={{ transformOrigin: '110px 65px', transform: 'rotate(0deg)', willChange: 'transform', transition: 'transform 0.1s linear' }}>
                <polygon points="106,65 114,65 110,15" fill="#ef4444" />
                <polygon points="106,65 114,65 110,115" fill="#ffffff" />
                <circle cx="110" cy="65" r="4" fill="#111" stroke="#ffffff" strokeWidth="2" />
              </g>
            </svg>
            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', marginTop: '4px' }}>
              <span ref={headingTextRef} style={{ color: '#fff', fontSize: '24px', fontWeight: 800, fontFamily: 'monospace', letterSpacing: '-0.05em', lineHeight: '24px' }}>N 0°</span>
            </div>
          </div>
        </div>
        </Rnd>
      )}`;

// Insert before the closing div of GlobeMap
const insertionPoint = code.lastIndexOf('    </div>\\n  );\\n}');
if (insertionPoint !== -1) {
  code = code.slice(0, insertionPoint) + compassUI + '\\n' + code.slice(insertionPoint);
  fs.writeFileSync('src/components/GlobeMap.tsx', code);
  console.log('Successfully added compass UI');
} else {
  console.log('Could not find insertion point');
}
