import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = re.sub(
    r'<path d=\{fullSvgPath\}.*?/>',
    r'<path ref={fullSvgPathRef} fill="none" stroke={animationProgress === 0 ? routeColor : \'rgba(255, 255, 255, 0.3)\'} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />',
    content
)

content = re.sub(
    r'\{inactiveSvgPath && <path d=\{inactiveSvgPath\}.*?/>\}',
    r'',
    content
)

content = re.sub(
    r'<path d=\{svgPath\}.*?/>',
    r'<path ref={svgPathRef} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5} strokeLinecap="round" strokeLinejoin="round" style={{ filter: \'drop-shadow(0 0 8px rgba(204,255,0,0.8))\' }} />',
    content
)

content = re.sub(
    r'\{svgPath && <path ref=\{svgPathRef\}.*?/>\}',
    r'<path ref={svgPathRef} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5} strokeLinecap="round" strokeLinejoin="round" style={{ filter: \'drop-shadow(0 0 8px rgba(204,255,0,0.8))\' }} />',
    content
)

# And the old distanceBadge JSX if it's still there
content = re.sub(
    r'\{vehicleDot && \(\s*<div.*?transform: \'translate\(-50%, -50%\)\'.*?/>\s*\)\}',
    r"""<div 
        ref={vehicleDotRef}
        className="absolute w-4 h-4 bg-[#CCFF00] rounded-full border-2 border-black pointer-events-none z-20"
        style={{ 
          top: 0, left: 0,
          marginLeft: '-8px', marginTop: '-8px',
          display: 'none',
          boxShadow: '0 0 10px rgba(204,255,0,0.5)',
          willChange: 'transform'
        }}
      />""",
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'\{distanceBadge && \(\s*<div.*?-ml-16 -mt-12.*?\{distanceBadge\.text\}.*?\{distanceBadge\.text2\}.*?</div>\s*\)\}',
    r"""<div 
        ref={distanceBadgeRef}
        className="absolute pointer-events-none z-30 flex items-center justify-center -ml-16 -mt-12"
        style={{ top: 0, left: 0, display: 'none', willChange: 'transform' }}
      >
        <div className="bg-black/80 backdrop-blur-md text-white text-[10px] font-mono px-3 py-1.5 rounded-full border border-[#CCFF00]/30 shadow-lg flex items-center gap-2">
          <span ref={distanceTextRef} className="text-[#CCFF00] font-bold"></span>
          <div className="w-px h-3 bg-white/20" />
          <span ref={distanceTimeRef} className="text-gray-300"></span>
        </div>
      </div>""",
    content,
    flags=re.DOTALL
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
