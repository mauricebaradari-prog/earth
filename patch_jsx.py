import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace SVG markup
old_svg = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor="#CCFF00" />
          </linearGradient>
        </defs>
        <path d={fullSvgPath} fill="none" stroke={animationProgress === 0 ? routeColor : 'rgba(255, 255, 255, 0.3)'} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
        {inactiveSvgPath && <path d={inactiveSvgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" opacity={0.5} />}
        {svgPath && <path d={svgPath} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5} strokeLinecap="round" strokeLinejoin="round" style={{ filter: 'drop-shadow(0 0 8px rgba(204,255,0,0.8))' }} />}
      </svg>"""

new_svg = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor="#CCFF00" />
          </linearGradient>
        </defs>
        <path ref={fullSvgPathRef} fill="none" stroke={animationProgress === 0 ? routeColor : 'rgba(255, 255, 255, 0.3)'} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
        <path ref={svgPathRef} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5} strokeLinecap="round" strokeLinejoin="round" style={{ filter: 'drop-shadow(0 0 8px rgba(204,255,0,0.8))' }} />
      </svg>"""
content = content.replace(old_svg, new_svg)

# Replace Vehicle Dot and Distance Badge
old_badge = """      {vehicleDot && (
        <div 
          className="absolute w-4 h-4 bg-[#CCFF00] rounded-full border-2 border-black pointer-events-none z-20"
          style={{ 
            left: vehicleDot.x, 
            top: vehicleDot.y, 
            transform: 'translate(-50%, -50%)',
            boxShadow: '0 0 10px rgba(204,255,0,0.5)'
          }}
        />
      )}

      {distanceBadge && (
        <div 
          className="absolute pointer-events-none z-30 flex items-center justify-center -ml-16 -mt-12"
          style={{ left: distanceBadge.x, top: distanceBadge.y }}
        >
          <div className="bg-black/80 backdrop-blur-md text-white text-[10px] font-mono px-3 py-1.5 rounded-full border border-[#CCFF00]/30 shadow-lg flex items-center gap-2">
            <span className="text-[#CCFF00] font-bold">{distanceBadge.text}</span>
            <div className="w-px h-3 bg-white/20" />
            <span className="text-gray-300">{distanceBadge.text2}</span>
          </div>
        </div>
      )}"""

new_badge = """      <div 
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
        className="absolute pointer-events-none z-30 flex items-center justify-center -ml-16 -mt-12"
        style={{ top: 0, left: 0, display: 'none', willChange: 'transform' }}
      >
        <div className="bg-black/80 backdrop-blur-md text-white text-[10px] font-mono px-3 py-1.5 rounded-full border border-[#CCFF00]/30 shadow-lg flex items-center gap-2">
          <span ref={distanceTextRef} className="text-[#CCFF00] font-bold"></span>
          <div className="w-px h-3 bg-white/20" />
          <span ref={distanceTimeRef} className="text-gray-300"></span>
        </div>
      </div>"""

content = content.replace(old_badge, new_badge)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
