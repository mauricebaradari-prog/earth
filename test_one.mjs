import exifr from 'exifr';
const fullPath = '/Users/mauricebaradari/Library/CloudStorage/GoogleDrive-maurice.baradari@gmail.com/Meine Ablage/GPS Images/img_1789760068429.jpg';

async function run() {
    const exif = await exifr.parse(fullPath);
    console.log("Latitude:", exif.latitude);
    console.log("Longitude:", exif.longitude);
}
run();
