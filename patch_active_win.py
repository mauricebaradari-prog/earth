import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

content = content.replace(
    "const [activeWindow, setActiveWindow] = useState<'elevation' | 'youtube' | 'chat'>('chat');",
    "const [activeWindow, setActiveWindow] = useState<'elevation' | 'youtube' | 'chat' | 'velocity'>('chat');"
)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
