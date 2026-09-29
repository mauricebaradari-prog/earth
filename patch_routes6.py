import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace('window.__ON_ROUTE_SELECT', '(window as any).__ON_ROUTE_SELECT')
content = content.replace('window.__ON_SEEK', '(window as any).__ON_SEEK')
content = content.replace('window.__ROUTE_COORDS', '(window as any).__ROUTE_COORDS')

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
