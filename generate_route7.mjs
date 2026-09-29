const url = "https://www.google.com/maps/dir/34.8510744,32.3838098/34.8533107,32.3853003/34.859841,32.3934698/34.8622366,32.4056227/34.8720869,32.4121196/34.8874491,32.4224393/34.8895975,32.4241108/34.8964556,32.4282424/34.9041933,32.429519/34.9124377,32.4256776";
const match = url.match(/dir\/([\d\.,\/]+)/);
if (match) {
    const coords = match[1].split('/').filter(x => x.includes(','));
    const cities = coords.map((c, i) => {
        const [lat, lng] = c.split(',');
        let name = `WP ${i}`;
        if (i === 0) name = "Pegeia";
        if (i === coords.length - 1) name = "Kathikas";
        return `      { id: 'wp7-${i}', name: '${name}', country: 'Cyprus', lat: ${lat}, lng: ${lng} }`;
    });
    console.log(`  {\n    id: 'route-7',\n    name: 'Pegeia → Kathikas',\n    videoId: 'E0QOwjdIuzY',\n    durationSeconds: 17 * 60 + 20, // 17:20\n    routeColor: '#CCFF00',\n    cities: [\n${cities.join(',\n')}\n    ]\n  }`);
}
