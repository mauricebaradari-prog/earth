with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

import re

# We want to replace the whole route-9 object
new_route = open('new_route9.txt').read()

# Using regex to find from "id: 'route-9'" down to the matching brackets
# The previous state is:
old = """    id: 'route-9',
    name: 'Kouklia → Pissouri',
    videoId: '9uLRToTIAyc',
    durationSeconds: 11 * 60 + 27, // 11:27
    routeColor: '#CCFF00',
    cities: [
      { id: 'wp9-0', name: 'Kouklia', country: 'Cyprus', lat: 34.6869276, lng: 32.5833376 },
      { id: 'wp9-1', name: 'Petra tou Romiou', country: 'Cyprus', lat: 34.6657239, lng: 32.6289967 },
      { id: 'wp9-b6-1', name: 'B6 Country Road 1', country: 'Cyprus', lat: 34.6607716, lng: 32.6524475 },
      { id: 'wp9-b6-2', name: 'B6 Country Road 2', country: 'Cyprus', lat: 34.6727244, lng: 32.6851291 },
      { id: 'wp9-2', name: 'Pissouri', country: 'Cyprus', lat: 34.674622, lng: 32.6962141 }
    ]"""

content = content.replace(old, new_route)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
