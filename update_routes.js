const fs = require('fs');

let code = fs.readFileSync('src/hooks/useEditorState.ts', 'utf8');

const newRoute = `
  {
    id: 'route-3',
    name: 'Kouklia → Agios Nikolaos',
    cities: [
      { id: 'r3-1', name: 'Kouklia', country: 'Cyprus', lat: 34.7149022, lng: 32.5501062 },
      { id: 'r3-2', name: 'Nikokleia', country: 'Cyprus', lat: 34.7311708, lng: 32.5807008 },
      { id: 'r3-3', name: 'Kidasi', country: 'Cyprus', lat: 34.8254251, lng: 32.7260753 },
      { id: 'r3-4', name: 'Pretori', country: 'Cyprus', lat: 34.8376584, lng: 32.7366831 },
      { id: 'r3-5', name: 'Kato Archimandrita', country: 'Cyprus', lat: 34.8441119, lng: 32.7391511 },
      { id: 'r3-6', name: 'Agios Nikolaos', country: 'Cyprus', lat: 34.868518, lng: 32.7655225 },
    ],
    videoId: 'z65BD4UIwzQ',
    durationSeconds: 1801, // ~30 minutes
    routeColor: '#CCFF00',
  }
`;

// Insert after route-2
const insertionPoint = code.indexOf('id: \\'route-2\\'');
if (insertionPoint !== -1) {
  const endOfRoute2 = code.indexOf('},', code.indexOf('routeColor:', insertionPoint)) + 2;
  code = code.slice(0, endOfRoute2) + '\\n' + newRoute + ',' + code.slice(endOfRoute2);
  fs.writeFileSync('src/hooks/useEditorState.ts', code);
  console.log('Successfully added route-3');
} else {
  console.log('Could not find route-2');
}
