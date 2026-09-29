import re
with open('src/app/page.tsx', 'r') as f:
    content = f.read()

content = content.replace("              cities={state.cities}\n              mapStyle={state.mapStyle}", "              cities={state.cities}\n              routes={state.routes}\n              mapStyle={state.mapStyle}")

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
