import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

svg_patch = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGradient" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor={routeColor} />
          </linearGradient>
        </defs>
        <path d={fullSvgPath} fill="none" stroke="url(#routeGradient)" strokeWidth={routeWidth * 1.5 + 2} strokeOpacity={0.3} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke="url(#routeGradient)" strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
      </svg>"""

content = re.sub(r"      <svg xmlns=\"http://www\.w3\.org/2000/svg\" style=\{\{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 \}\}>.*?</svg>", svg_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
