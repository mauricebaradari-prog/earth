import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

update_patch = """  async function updateRouteData(map: MaplibreMap, passId: number) {
    let activeMergedCoords: number[][] = [];"""

content = content.replace("""  async function updateRouteData(map: MaplibreMap, passId: number) {
    if (!map.getSource('route') || !map.getSource('route-inactive')) return;
    
    let activeMergedCoords: number[][] = [];""", update_patch)

progress_patch = """  function updateRouteProgress(
    map: MaplibreMap,
    cs: City[],
    progress: number,
    totalDist: number,
    legDists: number[]
  ) {
    let remaining = progress;"""

content = content.replace("""  function updateRouteProgress(
    map: MaplibreMap,
    cs: City[],
    progress: number,
    totalDist: number,
    legDists: number[]
  ) {
    if (!map.getSource('route')) return;

    let remaining = progress;""", progress_patch)


with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
