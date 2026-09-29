import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

state_patch = """  const [svgPath, setSvgPath] = React.useState<string>('');
  const [fullSvgPath, setFullSvgPath] = React.useState<string>('');
  const [inactivePaths, setInactivePaths] = React.useState<{id: string, path: string}[]>([]);
  
  const fullActiveCoordsRef = useRef<GeoJSON.Feature[]>([]);
  const inactiveCoordsRef = useRef<{id: string, features: GeoJSON.Feature[]}[]>([]);"""

content = re.sub(r"  const \[svgPath, setSvgPath\] = React\.useState<string>\(''\);\n  const \[fullSvgPath, setFullSvgPath\] = React\.useState<string>\(''\);", state_patch, content)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
