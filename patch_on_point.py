import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

patch = """          if (vehicleLngLatRef.current) {
            const p = mapRef.current.project(vehicleLngLatRef.current);
            setVehicleDot({ x: p.x, y: p.y });
            if (onPoint1Projected) {
              onPoint1Projected(p.x, p.y);
            }
          }"""

content = content.replace("""          if (vehicleLngLatRef.current) {
            const p = mapRef.current.project(vehicleLngLatRef.current);
            setVehicleDot({ x: p.x, y: p.y });
          }""", patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
