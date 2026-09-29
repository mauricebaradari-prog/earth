import fs from 'fs';

const data = JSON.parse(fs.readFileSync('b6.json', 'utf8'));
let coords = [];
data.elements.forEach(el => {
    if (el.geometry) {
        el.geometry.forEach(node => {
            coords.push([node.lon, node.lat]);
        });
    }
});

// Sort coords roughly by longitude (West to East)
coords.sort((a, b) => a[0] - b[0]);

// Pick 5 intermediate points
const points = [];
for (let i = 1; i <= 5; i++) {
    const idx = Math.floor(coords.length * (i / 6));
    points.push(coords[idx]);
}
console.log(points);
