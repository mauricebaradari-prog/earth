import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_vel = """             if (velocityTextRef.current) {
                const segDistKm = getDistanceKm(p1[1], p1[0], p2[1], p2[0]);
                const timeSecs = currentDuration / Math.max(1, fullPts.length - 1);"""

new_vel = """             if (velocityTextRef.current) {
                const exactIdx = currentProgress * (fullPts.length - 1);
                const pIdx = Math.min(Math.floor(exactIdx), fullPts.length - 2);
                const wp1 = fullPts[pIdx];
                const wp2 = fullPts[pIdx + 1];
                let segDistKm = 0;
                if (wp1 && wp2) {
                   segDistKm = getDistanceKm(wp1[1], wp1[0], wp2[1], wp2[0]);
                }
                const timeSecs = currentDuration / Math.max(1, fullPts.length - 1);"""

content = content.replace(old_vel, new_vel)

# And fix Gauge and showVelocity
content = content.replace("showElevation,", "showElevation,\n  showVelocity,")
if "showVelocity?: boolean;" not in content:
    content = content.replace("showElevation?: boolean;", "showElevation?: boolean;\n  showVelocity?: boolean;")

if "Gauge" not in content[:1000]:
    content = content.replace("Mountain } from 'lucide-react';", "Mountain, Gauge } from 'lucide-react';")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
