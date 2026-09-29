import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

with open('good_block.txt', 'r') as f:
    good_block = f.read()

# Only keep addSource in initRouteLayers to hide MapLibre line but keep the source
good_block = re.sub(
    r'    if \(\!map\.getLayer\(\'route-glow\'\)\) \{.*?\n  \}',
    '  }',
    good_block,
    flags=re.DOTALL
)

content = re.sub(
    r'  function initRouteLayers\(map.*?function updateRouteProgress',
    good_block + '\n\n  function updateRouteProgress',
    content,
    flags=re.DOTALL
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
