const url = "https://www.google.com/maps/dir/34.9124625,32.4256641/34.9137808,32.4263643/34.925198,32.4381723/34.9435348,32.4465716/34.9522976,32.4487758/34.9520524,32.450501/34.9529159,32.451033/34.9575986,32.4507197/34.964114,32.4563567/34.9954017,32.5117372/@34.9949696,32.5121003";
const match = url.match(/dir\/([\d\.,\/]+)/);
if (match) {
    const coords = match[1].split('/').filter(x => x.includes(','));
    const cities = coords.map((c, i) => {
        const [lat, lng] = c.split(',');
        return `      { id: 'wp-${i}', name: 'WP ${i}', country: 'Cyprus', lat: ${lat}, lng: ${lng} }`;
    });
    console.log(`  {\n    id: 'route-6',\n    name: 'New Route',\n    videoId: 'mxQj61ZXZ9k',\n    durationSeconds: 2000,\n    routeColor: '#CCFF00',\n    cities: [\n${cities.join(',\n')}\n    ]\n  }`);
}
