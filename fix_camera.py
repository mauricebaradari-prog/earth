import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_code = """      } else if (cameraMode === 'follow') {
        targetBearing = headingOnPath(fullRouteCoordsRef.current, progress);
      }"""

new_code = """      } else if (cameraMode === 'follow') {
        // User requested no rotation for Follow mode, keep the current bearing or reset to 0
        // targetBearing = map.getBearing(); 
      }"""

content = content.replace(old_code, new_code)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
