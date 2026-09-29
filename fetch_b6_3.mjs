import fs from 'fs';

const q = `
[out:json];
way["ref"="B6"](34.650, 32.600, 34.685, 32.700);
out geom;
`;

fetch("https://overpass.kumi.systems/api/interpreter", {
    method: "POST",
    headers: { "User-Agent": "EarthApp/1.0 (test@example.com)" },
    body: "data=" + encodeURIComponent(q)
}).then(r => r.json()).then(data => {
    let coords = [];
    data.elements.forEach(el => {
        if (el.geometry) {
            el.geometry.forEach(node => {
                coords.push([node.lon, node.lat]);
            });
        }
    });
    fs.writeFileSync('b6_coords.json', JSON.stringify(coords));
    console.log("Found", coords.length, "points");
}).catch(console.error);
