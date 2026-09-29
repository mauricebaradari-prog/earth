import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

# Find the start and end of route-9
match = re.search(r"    id: 'route-9',\n    name: 'Kouklia → Pissouri',.*?(?=    ]\n  })    \]\n  }", content, re.DOTALL)
if not match:
    # Try simpler regex
    content = re.sub(r"    id: 'route-9',[\s\S]*?    \]\n  }", open('new_route9.txt').read(), content)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
