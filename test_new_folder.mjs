import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Desktop/Neuer Ordner 2';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

async function run() {
    console.log(`Found ${files.length} images.`);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        try {
            const exif = await exifr.parse(fullPath);
            if (exif && exif.latitude !== undefined && !isNaN(exif.latitude)) {
                console.log(`File: ${file} | Lat: ${exif.latitude}, Lng: ${exif.longitude} | Time: ${exif.DateTimeOriginal}`);
                console.log("Full GPS block:", {
                    GPSLatitude: exif.GPSLatitude,
                    GPSLatitudeRef: exif.GPSLatitudeRef,
                    GPSLongitude: exif.GPSLongitude,
                    GPSLongitudeRef: exif.GPSLongitudeRef
                });
            } else {
                console.log(`File: ${file} | GPS data missing or invalid (NaN)`);
                console.log(exif);
            }
        } catch (e) {
            console.error(`File: ${file} | Error: ${e.message}`);
        }
    }
}
run();
