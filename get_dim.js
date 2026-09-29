const fs = require('fs');
const buffer = fs.readFileSync('/Users/mauricebaradari/.gemini/antigravity/brain/51088b5e-43c9-4b70-807b-879a3ccf083d/.user_uploaded/media_1789985717701.jpg');
// Super simple JPEG dimension parser
let i = 2;
while (i < buffer.length) {
    let marker = buffer.readUInt16BE(i);
    i += 2;
    if (marker >= 0xFFC0 && marker <= 0xFFC3) {
        i += 3;
        let h = buffer.readUInt16BE(i);
        let w = buffer.readUInt16BE(i + 2);
        console.log(`Dimensions: ${w}x${h}`);
        break;
    } else {
        i += buffer.readUInt16BE(i);
    }
}
