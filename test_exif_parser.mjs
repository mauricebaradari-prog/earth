import fs from 'fs';
import parser from 'exif-parser';

const fullPath = '/Users/mauricebaradari/Desktop/Neuer Ordner 2/img_1789749970398.jpg';
const buffer = fs.readFileSync(fullPath);
try {
    const parsed = parser.create(buffer).parse();
    console.log("exif-parser result:", parsed.tags);
} catch(e) {
    console.error("exif-parser error:", e);
}
