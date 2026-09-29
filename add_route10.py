import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

new_route = """    {
      id: 10,
      name: 'Kelokedara \u2192 Kidasi',
      cities: [
        { id: 'kelokedara', name: 'Kelokedara', coordinates: [32.4831292, 34.8777649] },
        { id: 'kidasi_w', name: 'Kidasi (West)', coordinates: [32.5843096, 34.9248352] },
        { id: 'kidasi', name: 'Kidasi', coordinates: [32.5890359, 34.9248475] }
      ],
      videoId: 'Febo-2Vx-Vs',
      durationSeconds: 931
    }
  ]"""

content = content.replace("    }\n  ]", new_route)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
