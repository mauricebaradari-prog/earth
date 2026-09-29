const fs = require('fs');
const exifParser = require('exif-parser');

try {
  const buffer = fs.readFileSync('/Users/mauricebaradari/.gemini/antigravity/brain/51088b5e-43c9-4b70-807b-879a3ccf083d/.user_uploaded/media_1789985717701.jpg');
  const parser = exifParser.create(buffer);
  const result = parser.parse();
  console.log(JSON.stringify(result.tags, null, 2));
} catch (e) {
  console.error('Error parsing EXIF:', e.message);
}
