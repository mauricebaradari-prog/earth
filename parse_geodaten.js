const fs = require('fs');
const path = require('path');
const exifParser = require('exif-parser');

const dir = '/Users/mauricebaradari/Desktop/geodaten';
const files = fs.readdirSync(dir).filter(f => f.endsWith('.jpg')).sort();
const route = [];

for (const file of files) {
    const buffer = fs.readFileSync(path.join(dir, file));
    try {
        const parser = exifParser.create(buffer);
        const result = parser.parse();
        if (result.tags && result.tags.GPSLatitude && result.tags.GPSLongitude) {
            route.push({
                file: file,
                lat: result.tags.GPSLatitude,
                lng: result.tags.GPSLongitude
            });
            console.log(`Parsed ${file}: [${result.tags.GPSLongitude}, ${result.tags.GPSLatitude}]`);
        } else {
            console.log(`No GPS data in ${file}`);
        }
    } catch (e) {
        console.error(`Error parsing ${file}:`, e.message);
    }
}

if (route.length > 0) {
    const geojson = route.map(p => [p.lng, p.lat]);
    fs.writeFileSync('public/gps_route.json', JSON.stringify(geojson, null, 2));
    console.log(`\nSuccessfully wrote ${route.length} points to public/gps_route.json`);
} else {
    console.log('\nNo points found.');
}
