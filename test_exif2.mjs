import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/Gps images';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

async function run() {
    let checked = 0;
    for (const file of files) {
        const fullPath = path.join(dir, file);
        try {
            const exif = await exifr.parse(fullPath);
            if (exif && exif.latitude && !isNaN(exif.latitude)) {
                console.log("Found valid GPS in:", file);
                console.log("Lat:", exif.latitude, "Lng:", exif.longitude);
                return;
            }
        } catch (e) {
        }
        checked++;
        if (checked > 50) break;
    }
    console.log("No valid GPS found in first 50 images.");
}
run();
