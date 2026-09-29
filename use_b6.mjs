import fs from 'fs';
const coords = JSON.parse(fs.readFileSync('b6_coords.json', 'utf8'));
// Sort west to east
coords.sort((a, b) => a[0] - b[0]);
// Pick 30 points evenly distributed to act as waypoints
const waypoints = [];
for(let i=0; i<30; i++) {
    const idx = Math.floor(i * (coords.length / 30));
    waypoints.push({ lat: coords[idx][1], lng: coords[idx][0] });
}
let str = `    id: 'route-9',
    name: 'Kouklia → Pissouri',
    videoId: '9uLRToTIAyc',
    durationSeconds: 11 * 60 + 27, // 11:27
    routeColor: '#CCFF00',
    forceStraight: true,
    cities: [\n`;
str += `      { id: 'wp9-0', name: 'Kouklia', country: 'Cyprus', lat: 34.6869276, lng: 32.5833376 },\n`;
str += `      { id: 'wp9-1', name: 'Petra tou Romiou', country: 'Cyprus', lat: 34.6657239, lng: 32.6289967 },\n`;
waypoints.forEach((p, i) => {
    str += `      { id: 'wp9-coast-${i}', name: 'B6 Coast', country: 'Cyprus', lat: ${p.lat}, lng: ${p.lng} },\n`;
});
str += `      { id: 'wp9-2', name: 'Pissouri', country: 'Cyprus', lat: 34.674622, lng: 32.6962141 }\n`;
str += `    ]`;
fs.writeFileSync('new_route9.txt', str);
