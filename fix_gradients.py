import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# 1. Update the SVG paths for the main route
svg_block = """      <svg xmlns="http://www.w3.org/2000/svg" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%', pointerEvents: 'none', zIndex: 10 }}>
        <defs>
          <linearGradient id="routeGrad" x1="0" y1="0" x2="1" y2="0">
            <stop offset="0%" stopColor="#FFFFFF" />
            <stop offset="100%" stopColor="#CCFF00" />
          </linearGradient>
        </defs>
        <path d={fullSvgPath} fill="none" stroke="rgba(255, 255, 255, 0.3)" strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />
        <path d={svgPath} fill="none" stroke="url(#routeGrad)" strokeWidth={routeWidth * 1.5 + 2} strokeLinecap="round" strokeLinejoin="round" />"""

content = re.sub(
    r'<svg xmlns="http://www.w3.org/2000/svg"[^>]*>.*?<path d=\{svgPath\}[^>]*>',
    svg_block,
    content,
    flags=re.DOTALL
)

# 2. Update Elevation Profile gradients
elev_grad_block = """                      <defs>
                        <linearGradient id="elevGrad" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#FFFFFF" stopOpacity={0.6} />
                          <stop offset="100%" stopColor="#CCFF00" stopOpacity={0.6} />
                        </linearGradient>
                        <linearGradient id="elevStrokeGrad" x1="0" y1="0" x2="1" y2="0">
                          <stop offset="0%" stopColor="#FFFFFF" />
                          <stop offset="100%" stopColor="#CCFF00" />
                        </linearGradient>
                      </defs>
                      <path d={pathData} fill="url(#elevGrad)" className="pointer-events-none" />
                      <path d={lineData} fill="none" stroke="url(#elevStrokeGrad)" strokeWidth="2" strokeLinejoin="round" className="pointer-events-none" />"""

content = re.sub(
    r'<defs>\s*<linearGradient id="elevGrad".*?</linearGradient>\s*</defs>\s*<path d=\{pathData\}[^>]*>\s*<path d=\{lineData\}[^>]*>',
    elev_grad_block,
    content,
    flags=re.DOTALL
)

# 3. Disable Maplibre Map route-glow to avoid conflict with SVG fully-visible route issue
content = content.replace("initRouteLayers(map, routeColor, routeWidth);", "// initRouteLayers(map, routeColor, routeWidth);")


with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
