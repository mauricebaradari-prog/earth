import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

old_effect = """  }, [animationProgress, cities, useGpsTrace, routes]);"""
new_effect = """  }, [animationProgress]);"""

content = content.replace(old_effect, new_effect)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
