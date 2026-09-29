import exifr from 'exifr';
const fullPath = '/Users/mauricebaradari/Desktop/Neuer Ordner 3/img_1789760080789.jpg';

async function run() {
    const exif = await exifr.parse(fullPath);
    console.log("Latitude:", exif.latitude);
    console.log("Longitude:", exif.longitude);
}
run();
