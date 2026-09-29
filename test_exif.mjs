import fs from 'fs';
import path from 'path';
import exifr from 'exifr';

const dir = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/Gps images';
const files = fs.readdirSync(dir).filter(f => f.match(/\.(jpe?g|png|heic)$/i));

async function run() {
    if (files.length === 0) return;
    const fullPath = path.join(dir, files[0]);
    console.log("Parsing:", files[0]);
    try {
        const exif = await exifr.parse(fullPath);
        console.log("Parsed:", exif);
    } catch (e) {
        console.error(e);
    }
}
run();
