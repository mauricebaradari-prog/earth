import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_p1 = """             // Only call if it moved significantly to avoid spam
             if (!(window as any)._lastP1 || Math.abs((window as any)._lastP1.x - p1.x) > 10 || Math.abs((window as any)._lastP1.y - p1.y) > 10) {
               (window as any)._lastP1 = { x: p1.x, y: p1.y };
               onPoint1Projected(p1.x, p1.y);
             }"""

new_p1 = """             // Only call if it moved significantly to avoid spam
             if (!(window as any)._lastP1 || Math.abs((window as any)._lastP1.x - p1.x) > 10 || Math.abs((window as any)._lastP1.y - p1.y) > 10) {
               (window as any)._lastP1 = { x: p1.x, y: p1.y };
               Promise.resolve().then(() => onPoint1Projected(p1.x, p1.y));
             }"""

content = content.replace(old_p1, new_p1)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
