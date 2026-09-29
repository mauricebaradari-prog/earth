import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "activeWindow?: 'video' | 'elevation' | null;",
    "activeWindow?: 'video' | 'elevation' | 'velocity' | null;"
)
content = content.replace(
    "setActiveWindow?: (win: 'video' | 'elevation') => void;",
    "setActiveWindow?: (win: 'video' | 'elevation' | 'velocity') => void;"
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
