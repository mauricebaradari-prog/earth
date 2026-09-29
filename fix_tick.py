import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

content = content.replace(
    "if (Math.abs(prev.animationProgress - next) < 0.0001) return prev;",
    "// Removed threshold check because long routes move less than 0.0001 per frame"
)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
