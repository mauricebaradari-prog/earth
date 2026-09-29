import fs from 'fs';
import exifr from 'exifr';

const fullPath = '/Users/mauricebaradari/.gemini/antigravity/brain/51088b5e-43c9-4b70-807b-879a3ccf083d/.user_uploaded/media_1789750051434.jpg';

async function run() {
    try {
        const exif = await exifr.parse(fullPath);
        if (exif) {
            console.log("Parsed EXIF:");
            console.log("Latitude:", exif.latitude);
            console.log("Longitude:", exif.longitude);
            console.log("DateTime:", exif.DateTimeOriginal);
            console.log("Full GPS block:", {
                GPSLatitude: exif.GPSLatitude,
                GPSLatitudeRef: exif.GPSLatitudeRef,
                GPSLongitude: exif.GPSLongitude,
                GPSLongitudeRef: exif.GPSLongitudeRef
            });
        } else {
            console.log("No EXIF data found.");
        }
    } catch (e) {
        console.error("Error:", e.message);
    }
}
run();
