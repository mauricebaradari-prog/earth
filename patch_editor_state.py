import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

content = content.replace(
    "activeWindow: 'video' | 'elevation' | null;",
    "activeWindow: 'video' | 'elevation' | 'velocity' | null;"
)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
