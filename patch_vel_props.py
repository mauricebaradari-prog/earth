import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("  showElevation?: boolean;", "  showElevation?: boolean;\n  showVelocity?: boolean;")
content = content.replace("  showElevation = true,", "  showElevation = true,\n  showVelocity = true,")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
