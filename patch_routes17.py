import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Remove the svg paths that draw the route, but keep the vehicle marker and distance badge
svg_patch = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        {/* SVG overlay is now only used for positioning HTML elements. MapLibre natively renders the route lines with gradients! */}
      </svg>"""

content = re.sub(r"      <svg xmlns=\"http://www\.w3\.org/2000/svg\" style=\{\{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 \}\}>.*?      </svg>", svg_patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
