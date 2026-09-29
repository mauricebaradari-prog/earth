import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

replacement = """      {showElevation && elevationProfile && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 340 : 0, y: 20, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '16px' }} className="pointer-events-none">"""

content = re.sub(
    r'      \{showElevation && elevationProfile && \(\n        <div style=\{\{ position: \'absolute\', top: 20, right: 20,.*?>\n          <div style=\{\{ display: \'flex\', justifyContent: \'space-between\', alignItems: \'flex-start\', marginBottom: \'16px\' \}\}>',
    replacement,
    content,
    flags=re.DOTALL
)

# Replace the closing div with closing Rnd
content = re.sub(
    r'            </div>\n          </div>\n        </div>\n      \)\}',
    r'            </div>\n          </div>\n        </div>\n        </Rnd>\n      )}',
    content,
    flags=re.DOTALL
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
