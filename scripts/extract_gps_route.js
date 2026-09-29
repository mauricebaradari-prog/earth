#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const exifParser = require('exif-parser');

const args = process.argv.slice(2);
if (args.length < 2) {
    console.error('Usage: node scripts/extract_gps_route.js <input_directory> <output_json_file>');
    console.error('Example: node scripts/extract_gps_route.js /Users/mauricebaradari/Desktop/geodaten public/route_10.json');
    process.exit(1);
}

const inputDir = args[0];
const outputFile = args[1];

if (!fs.existsSync(inputDir)) {
    console.error(`Error: Input directory does not exist: ${inputDir}`);
    process.exit(1);
}

// Find all jpeg files
const files = fs.readdirSync(inputDir)
    .filter(f => f.toLowerCase().endsWith('.jpg') || f.toLowerCase().endsWith('.jpeg'))
    // Sort alphabetically (which sorts chronologically if named with timestamps like img_12345.jpg)
    .sort();

if (files.length === 0) {
    console.error(`No JPEG images found in ${inputDir}`);
    process.exit(1);
}

console.log(`Found ${files.length} images. Extracting GPS data...`);

const route = [];
let missing = 0;

for (const file of files) {
    const filePath = path.join(inputDir, file);
    try {
        const buffer = fs.readFileSync(filePath);
        const parser = exifParser.create(buffer);
        const result = parser.parse();
        
        if (result.tags && result.tags.GPSLatitude && result.tags.GPSLongitude) {
            route.push([result.tags.GPSLongitude, result.tags.GPSLatitude]);
        } else {
            missing++;
        }
    } catch (e) {
        console.error(`Error parsing ${file}: ${e.message}`);
        missing++;
    }
}

if (route.length > 0) {
    fs.writeFileSync(outputFile, JSON.stringify(route, null, 2));
    console.log(`\nSuccess! Wrote ${route.length} GPS points to ${outputFile}`);
    if (missing > 0) {
        console.warn(`Note: ${missing} images were missing GPS data or couldn't be parsed.`);
    }
} else {
    console.error('\nFailed: No GPS data could be extracted from any of the images.');
}
