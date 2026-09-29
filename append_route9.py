with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

with open('new_route9.txt', 'r') as f:
    new_route = f.read() + ",\n];"

content = content.replace("];\n\nfunction getActiveRoute", new_route + "\n\nfunction getActiveRoute")

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
