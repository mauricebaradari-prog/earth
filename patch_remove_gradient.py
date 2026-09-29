import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

svg_patch = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <path d={fullSvgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeOpacity={0.3} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke={routeColor} strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
      </svg>"""

content = re.sub(r"      <svg xmlns=\"http://www\.w3\.org/2000/svg\" style=\{\{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 \}\}>.*?</svg>", svg_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
