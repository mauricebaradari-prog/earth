import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

patch = """    // Update gradient so the line grows
    const safeProgress = Math.max(0.001, Math.min(progress, 0.999));
    const gradient = [
      'interpolate',
      ['linear'],
      ['line-progress'],
      0, '#FFFFFF',
      safeProgress, routeColor,
      safeProgress + 0.0001, 'rgba(255,255,255,0.3)',
      1, 'rgba(255,255,255,0.3)'
    ];"""

content = re.sub(r'    // Update gradient so the line grows.*?1, \'rgba\(255,255,255,0\)\'\n    \];', patch, content, flags=re.DOTALL)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
