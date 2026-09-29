import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

log_patch = """
    console.log('UPDATING ROUTE DATA. Active:', activeRouteId, 'Inactive Features:', inactiveFeatures.length, 'Active features:', activeFeatures.length);
    if (map.getSource('route-inactive')) {
"""

content = content.replace("    if (map.getSource('route-inactive')) {", log_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
