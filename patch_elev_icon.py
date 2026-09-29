import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_header = """            <div>
              <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: '0 0 4px 0', fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Elevation Profile</h3>
              <div style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif', display: 'flex', alignItems: 'center', gap: '6px' }}>"""

new_header = """            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                <Mountain size={14} className="text-[#CCFF00]" />
                <h3 style={{ color: '#fff', fontSize: '11px', fontWeight: 700, letterSpacing: '0.05em', margin: 0, fontFamily: 'sans-serif', textTransform: 'uppercase' }}>Elevation Profile</h3>
              </div>
              <div style={{ color: '#9ca3af', fontSize: '10px', fontWeight: 500, fontFamily: 'sans-serif', display: 'flex', alignItems: 'center', gap: '6px' }}>"""

content = content.replace(old_header, new_header)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
