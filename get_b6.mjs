const query = `
[out:json];
way
  ["highway"]
  (34.650, 32.625, 34.685, 32.700);
out geom;
`;
// Wait, name="B6" might not be applied everywhere. Let's just fetch name="B6" first.
const q2 = `
[out:json];
way["ref"="B6"](34.650, 32.625, 34.685, 32.700);
out geom;
`;

fetch("http://overpass-api.de/api/interpreter", {
    method: "POST",
    body: "data=" + encodeURIComponent(q2)
}).then(r => r.json()).then(data => {
    let coords = [];
    data.elements.forEach(el => {
        if (el.type === 'way') {
            el.geometry.forEach(node => {
                coords.push([node.lon, node.lat]);
            });
        }
    });
    console.log(JSON.stringify(coords.slice(0, 5)));
    console.log("Total points:", coords.length);
    import('fs').then(fs => fs.writeFileSync('b6_coords.json', JSON.stringify(coords)));
}).catch(console.error);
