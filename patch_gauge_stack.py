import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_block = """          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '140px' }} className="pointer-events-none">
            <svg width="220" height="115" viewBox="0 0 220 115" style={{ overflow: 'visible' }}>
              <defs>
                <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#ef4444" />
                  <stop offset="50%" stopColor="#eab308" />
                  <stop offset="100%" stopColor="#22c55e" />
                </linearGradient>
              </defs>
              <path d="M 30 90 A 80 80 0 0 1 190 90" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="12" strokeLinecap="round" />
              <path d="M 30 90 A 80 80 0 0 1 190 90" fill="none" stroke="url(#gaugeGrad)" strokeWidth="12" strokeLinecap="round" />
              
              <g ref={velocityNeedleRef} style={{ transformOrigin: '110px 90px', transform: 'rotate(-90deg)', willChange: 'transform', transition: 'transform 0.1s linear' }}>
                <polygon points="107,90 113,90 110,25" fill="#ffffff" />
                <circle cx="110" cy="90" r="5" fill="#111" stroke="#ffffff" strokeWidth="2" />
              </g>
              
              <text x="30" y="112" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">0</text>
              <text x="110" y="32" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">75</text>
              <text x="190" y="112" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">150</text>
            </svg>
            <div style={{ width: '100%', display: 'flex', justifyContent: 'center', alignItems: 'baseline', gap: '4px', marginTop: '4px' }}>
              <span ref={velocityTextRef} style={{ color: '#fff', fontSize: '32px', fontWeight: 800, fontFamily: 'monospace', letterSpacing: '-0.05em', lineHeight: '32px' }}>0</span>
              <span style={{ color: '#9ca3af', fontSize: '13px', fontWeight: 600 }}>km/h</span>
            </div>
          </div>"""

new_block = """          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', width: '100%', height: '170px' }} className="pointer-events-none">
            <svg width="220" height="115" viewBox="0 0 220 115" style={{ overflow: 'visible' }}>
              <defs>
                <linearGradient id="gaugeGrad" x1="0" y1="0" x2="1" y2="0">
                  <stop offset="0%" stopColor="#ef4444" />
                  <stop offset="50%" stopColor="#eab308" />
                  <stop offset="100%" stopColor="#22c55e" />
                </linearGradient>
              </defs>
              <path d="M 30 90 A 80 80 0 0 1 190 90" fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth="12" strokeLinecap="round" />
              <path d="M 30 90 A 80 80 0 0 1 190 90" fill="none" stroke="url(#gaugeGrad)" strokeWidth="12" strokeLinecap="round" />
              
              <g ref={velocityNeedleRef} style={{ transformOrigin: '110px 90px', transform: 'rotate(-90deg)', willChange: 'transform', transition: 'transform 0.1s linear' }}>
                <polygon points="107,90 113,90 110,25" fill="#ffffff" />
                <circle cx="110" cy="90" r="5" fill="#111" stroke="#ffffff" strokeWidth="2" />
              </g>
              
              <text x="30" y="112" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">0</text>
              <text x="110" y="32" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">75</text>
              <text x="190" y="112" fill="#6b7280" fontSize="11" fontFamily="sans-serif" fontWeight="700" textAnchor="middle">150</text>
            </svg>
            <div style={{ width: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center', marginTop: '4px' }}>
              <span ref={velocityTextRef} style={{ color: '#fff', fontSize: '36px', fontWeight: 800, fontFamily: 'monospace', letterSpacing: '-0.05em', lineHeight: '36px' }}>0</span>
              <span style={{ color: '#9ca3af', fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', marginTop: '2px' }}>km/h</span>
            </div>
          </div>"""

content = content.replace(old_block, new_block)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
