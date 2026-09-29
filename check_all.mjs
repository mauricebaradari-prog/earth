import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/Gps images';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

async function run() {
    let nanCount = 0;
    let missingCount = 0;
    let validCount = 0;
    for (const file of files) {
        const fullPath = path.join(dir, file);
        try {
            const exif = await exifr.parse(fullPath);
            if (exif && exif.latitude !== undefined) {
                if (isNaN(exif.latitude)) {
                    nanCount++;
                } else {
                    validCount++;
                }
            } else {
                missingCount++;
            }
        } catch (e) {
            missingCount++;
        }
    }
    console.log(`Valid: ${validCount}, NaN: ${nanCount}, Missing: ${missingCount}`);
}
run();
