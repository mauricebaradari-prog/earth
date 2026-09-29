import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

new_route = """    ]
  },
  {
    id: 'route-10',
    name: 'Kelokedara \u2192 Kidasi',
    cities: [
      { id: 'r10-1', name: 'Kelokedara', country: 'Cyprus', lat: 34.8777649, lng: 32.4831292 },
      { id: 'r10-2', name: 'Kidasi (West)', country: 'Cyprus', lat: 34.9248352, lng: 32.5843096 },
      { id: 'r10-3', name: 'Kidasi', country: 'Cyprus', lat: 34.9248475, lng: 32.5890359 }
    ],
    videoId: 'Febo-2Vx-Vs',
    durationSeconds: 931,
    routeColor: '#CCFF00',
    forceStraight: false
  }
];"""

content = content.replace("    ]\n  }\n,\n];", new_route)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
