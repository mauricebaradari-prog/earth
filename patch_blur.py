import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Make both panels more transparent to highlight the blur effect
content = content.replace(
    "background: 'linear-gradient(180deg, rgba(17,17,17,0.95) 0%, rgba(17,17,17,0.85) 100%)'",
    "background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)'"
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
