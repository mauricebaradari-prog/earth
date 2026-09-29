import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Desktop/wetransfer_img_1789760099537-jpg_2026-09-18_1942';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

async function run() {
    console.log(`Found ${files.length} images.`);
    for (const file of files) {
        const fullPath = path.join(dir, file);
        try {
            const exif = await exifr.parse(fullPath);
            if (exif && exif.latitude !== undefined && !isNaN(exif.latitude)) {
                console.log(`SUCCESS! File: ${file} | Lat: ${exif.latitude}, Lng: ${exif.longitude} | Time: ${exif.DateTimeOriginal}`);
            } else {
                console.log(`FAILED! File: ${file} | GPS data missing or invalid (NaN)`);
            }
        } catch (e) {
            console.error(`Error: ${e.message}`);
        }
    }
}
run();
