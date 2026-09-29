const url = "https://www.google.com/maps/dir/34.6869276,32.5833376/34.6657239,32.6289967/34.674622,32.6962141";
const match = url.match(/dir\/([\d\.,\/]+)/);
if (match) {
    const coords = match[1].split('/').filter(x => x.includes(','));
    const cities = coords.map((c, i) => {
        const [lat, lng] = c.split(',');
        let name = `WP ${i}`;
        if (i === 0) name = "Kouklia";
        if (i === coords.length - 1) name = "Pissouri";
        return `      { id: 'wp9-${i}', name: '${name}', country: 'Cyprus', lat: ${lat}, lng: ${lng} }`;
    });
    console.log(`  {\n    id: 'route-9',\n    name: 'Kouklia → Pissouri',\n    videoId: '9uLRToTIAyc',\n    durationSeconds: 11 * 60 + 27, // 11:27\n    routeColor: '#CCFF00',\n    cities: [\n${cities.join(',\n')}\n    ]\n  }`);
}
