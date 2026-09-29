import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "setActiveWindow?: (w: 'video' | 'elevation') => void;",
    "setActiveWindow?: (w: 'video' | 'elevation' | 'velocity') => void;"
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
