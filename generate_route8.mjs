const url = "https://www.google.com/maps/dir/34.7758272,32.4097781/34.7768358,32.4072865/34.9028965,32.3179217";
const match = url.match(/dir\/([\d\.,\/]+)/);
if (match) {
    const coords = match[1].split('/').filter(x => x.includes(','));
    const cities = coords.map((c, i) => {
        const [lat, lng] = c.split(',');
        let name = `WP ${i}`;
        if (i === 0) name = "Paphos";
        if (i === coords.length - 1) name = "Agios Georgios";
        return `      { id: 'wp8-${i}', name: '${name}', country: 'Cyprus', lat: ${lat}, lng: ${lng} }`;
    });
    console.log(`  {\n    id: 'route-8',\n    name: 'Paphos → Agios Georgios',\n    videoId: '_FN0eryH4N8',\n    durationSeconds: 23 * 60 + 39, // 23:39\n    routeColor: '#CCFF00',\n    cities: [\n${cities.join(',\n')}\n    ]\n  }`);
}
