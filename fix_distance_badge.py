import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_jsx = """      <div 
        ref={vehicleDotRef}
        className="absolute w-4 h-4 bg-[#CCFF00] rounded-full border-2 border-black pointer-events-none z-20"
        style={{ 
          top: 0, left: 0,
          marginLeft: '-8px', marginTop: '-8px',
          display: 'none',
          boxShadow: '0 0 10px rgba(204,255,0,0.5)',
          willChange: 'transform'
        }}
      />"""

new_jsx = """      <div 
        ref={vehicleDotRef}
        className="absolute w-4 h-4 bg-[#CCFF00] rounded-full border-2 border-black pointer-events-none z-20"
        style={{ 
          top: 0, left: 0,
          marginLeft: '-8px', marginTop: '-8px',
          display: 'none',
          boxShadow: '0 0 10px rgba(204,255,0,0.5)',
          willChange: 'transform'
        }}
      />
      
      <div 
        ref={distanceBadgeRef}
        className="absolute pointer-events-none z-20 flex flex-col items-center justify-center bg-black/80 backdrop-blur-md rounded-lg border border-white/10 shadow-xl"
        style={{
          top: 0, left: 0,
          marginLeft: '-35px', marginTop: '-50px',
          width: '70px', padding: '4px',
          display: 'none',
          willChange: 'transform'
        }}
      >
        <span ref={distanceTextRef} className="text-[#CCFF00] font-bold text-xs">0 km</span>
        <span ref={distanceTimeRef} className="text-white/70 text-[10px] font-medium uppercase tracking-wider">0m 0s</span>
      </div>"""

content = content.replace(old_jsx, new_jsx)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
