import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Wrap containerRef
content = content.replace(
    '<div className="w-full h-full relative" ref={containerRef}>',
    '<div className="w-full h-full absolute inset-0 pointer-events-none z-0">\n      <div className="w-full relative pointer-events-auto" style={{ height: isMobile ? "40vh" : "100%" }} ref={containerRef}>'
)

# 2. Close containerRef before the first Rnd (Elevation)
start_elevation = '      {showElevation && elevationProfile && ('
content = content.replace(
    start_elevation,
    '      </div>\n' + start_elevation
)

# 3. Add closing div for the new outer wrapper at the very end
end_str = '        </Rnd>\n      )}\n    </div>\n  );\n}'
content = content.replace(
    end_str,
    '        </Rnd>\n      )}\n    </div>\n    </div>\n  );\n}'
)

# 4. Wrap ElevationProfile logic
elev_start_rnd = '''        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 24, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'elevation' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('elevation')}
          onMouseDown={() => setActiveWindow && setActiveWindow('elevation')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">'''

elev_end_rnd = '''        </div>
        </Rnd>'''

content = content.replace(
    '      {showElevation && elevationProfile && (',
    '      {showElevation && elevationProfile && (() => {\n        const content = ('
)

content = content.replace(
    elev_start_rnd,
    '''          <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)', borderRadius: isMobile ? '0' : '12px', border: isMobile ? 'none' : '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: isMobile ? 'default' : 'grab' }} className={isMobile ? "" : "active:cursor-grabbing"}>'''
)

content = content.replace(
    elev_end_rnd,
    '''          </div>
        );
        if (isMobile) {
          return (
            <div className="absolute left-0 w-full pointer-events-auto bg-black z-50 border-t border-white/10" style={{ top: '75vh', height: '25vh' }}>
              {content}
            </div>
          );
        }
        return (
          <Rnd
            default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 24, width: 320, height: 'auto' }}
            bounds="parent"
            enableResizing={false}
            className="z-50"
            style={{ zIndex: activeWindow === 'elevation' ? 60 : 50 }}
            onDragStart={() => setActiveWindow && setActiveWindow('elevation')}
            onMouseDown={() => setActiveWindow && setActiveWindow('elevation')}
          >
            {content}
          </Rnd>
        );
      })()'''
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
