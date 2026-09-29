import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

content = content.replace("import { EditorState, City } from '@/hooks/useEditorState';", "import { EditorState, City, ROUTES } from '@/hooks/useEditorState';")
content = content.replace("const _routes = routes || [];", "const _routes = routes && routes.length > 0 ? routes : ROUTES;")

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
