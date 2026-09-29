import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/Gps images';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

console.log(`Found ${files.length} images.`);

async function run() {
    let points = [];
    let count = 0;
    for (const file of files) {
        const fullPath = path.join(dir, file);
        try {
            // Read GPS and DateTimeOriginal
            const exif = await exifr.parse(fullPath, ['latitude', 'longitude', 'DateTimeOriginal', 'GPSDateStamp', 'GPSTimeStamp']);
            if (exif && exif.latitude && exif.longitude) {
                let timestamp = null;
                if (exif.DateTimeOriginal) {
                    timestamp = new Date(exif.DateTimeOriginal).getTime();
                } else if (exif.GPSDateStamp && exif.GPSTimeStamp) {
                    timestamp = new Date(`${exif.GPSDateStamp} ${exif.GPSTimeStamp}`).getTime();
                } else {
                    // fallback to file creation time
                    timestamp = fs.statSync(fullPath).birthtimeMs;
                }
                
                points.push({
                    file,
                    lat: exif.latitude,
                    lng: exif.longitude,
                    timestamp
                });
            }
        } catch (e) {
            console.error(`Error parsing ${file}: ${e.message}`);
        }
        count++;
        if (count % 10 === 0) {
            console.log(`Processed ${count}/${files.length} files...`);
        }
    }
    
    // Sort by timestamp
    points.sort((a, b) => a.timestamp - b.timestamp);
    
    fs.writeFileSync('public/gps_route.json', JSON.stringify(points, null, 2));
    console.log(`Successfully extracted ${points.length} GPS points and saved to public/gps_route.json.`);
}
run();
