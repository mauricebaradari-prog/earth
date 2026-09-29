import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

refs = """  const vehicleDotRef = React.useRef<HTMLDivElement>(null);
  const distanceBadgeRef = React.useRef<HTMLDivElement>(null);
  const distanceTextRef = React.useRef<HTMLSpanElement>(null);
  const distanceTimeRef = React.useRef<HTMLSpanElement>(null);
  const fullSvgPathRef = React.useRef<SVGPathElement>(null);
  const svgPathRef = React.useRef<SVGPathElement>(null);"""

content = content.replace("const osrmCacheRef = useRef<Record<string, [number, number][]>>({});", refs + "\n  const osrmCacheRef = useRef<Record<string, [number, number][]>>({});")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
