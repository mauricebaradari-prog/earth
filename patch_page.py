import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

content = re.sub(r'          routes=\{state\.routes\}\n', '', content)
content = re.sub(r'          activeRouteId=\{state\.activeRouteId\}\n', '', content)
content = re.sub(r'          onRouteSelect=\{setActiveRoute\}\n', '', content)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
