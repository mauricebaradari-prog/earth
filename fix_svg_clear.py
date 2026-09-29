import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_full = """          if (screenPts.length > 0 && fullSvgPathRef.current) {
             fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);
          }"""
new_full = """          if (fullSvgPathRef.current) {
             if (screenPts.length > 0) {
               fullSvgPathRef.current.setAttribute('d', `M ${screenPts.join(' L ')}`);
             } else {
               fullSvgPathRef.current.setAttribute('d', '');
             }
          }"""

old_svg = """          if (pts.length > 0 && svgPathRef.current) {
            svgPathRef.current.setAttribute('d', `M ${pts.join(' L ')}`);
          }"""
new_svg = """          if (svgPathRef.current) {
            if (pts.length > 0) {
              svgPathRef.current.setAttribute('d', `M ${pts.join(' L ')}`);
            } else {
              svgPathRef.current.setAttribute('d', '');
            }
          }"""

content = content.replace(old_full, new_full).replace(old_svg, new_svg)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
