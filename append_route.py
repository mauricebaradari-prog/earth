import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

new_route = """  {
    id: 'route-6',
    name: 'Kathikas → Lysos',
    cities: [
      { id: 'wp6-0', name: 'Kathikas', country: 'Cyprus', lat: 34.9124625, lng: 32.4256641 },
      { id: 'wp6-1', name: 'WP 1', country: 'Cyprus', lat: 34.9137808, lng: 32.4263643 },
      { id: 'wp6-2', name: 'WP 2', country: 'Cyprus', lat: 34.925198, lng: 32.4381723 },
      { id: 'wp6-3', name: 'WP 3', country: 'Cyprus', lat: 34.9435348, lng: 32.4465716 },
      { id: 'wp6-4', name: 'WP 4', country: 'Cyprus', lat: 34.9522976, lng: 32.4487758 },
      { id: 'wp6-5', name: 'WP 5', country: 'Cyprus', lat: 34.9520524, lng: 32.450501 },
      { id: 'wp6-6', name: 'WP 6', country: 'Cyprus', lat: 34.9529159, lng: 32.451033 },
      { id: 'wp6-7', name: 'WP 7', country: 'Cyprus', lat: 34.9575986, lng: 32.4507197 },
      { id: 'wp6-8', name: 'WP 8', country: 'Cyprus', lat: 34.964114, lng: 32.4563567 },
      { id: 'wp6-9', name: 'Lysos', country: 'Cyprus', lat: 34.9954017, lng: 32.5117372 }
    ],
    videoId: 'mxQj61ZXZ9k',
    durationSeconds: 30 * 60, // approximate 30 mins
    routeColor: '#CCFF00',
  },
];"""

content = content.replace("];\n\nexport function useEditorState()", new_route + "\n\nexport function useEditorState()")

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
