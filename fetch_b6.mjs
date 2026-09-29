import fs from 'fs';

const q = `
[out:json];
(
  way["ref"="B6"](34.650, 32.600, 34.685, 32.700);
  way["name"~"B6"](34.650, 32.600, 34.685, 32.700);
);
out geom;
`;

fetch("http://overpass-api.de/api/interpreter", {
    method: "POST",
    body: "data=" + encodeURIComponent(q)
}).then(r => r.json()).then(data => {
    let ways = [];
    data.elements.forEach(el => {
        if (el.geometry) {
            let coords = el.geometry.map(n => [n.lon, n.lat]);
            ways.push(coords);
        }
    });
    console.log("Ways found:", ways.length);
    fs.writeFileSync('b6_ways.json', JSON.stringify(ways));
}).catch(console.error);
