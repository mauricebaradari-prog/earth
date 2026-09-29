const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

// Change top-left to top-right
code = code.replace('className="absolute top-6 left-6 z-50 flex flex-col gap-4"', 'className="absolute top-6 right-6 z-50 flex flex-col items-end gap-4"');

// Change panel popout direction (from left-14 to right-14)
code = code.replace('className="absolute top-0 left-14 w-72 bg-black/80', 'className="absolute top-0 right-14 w-72 bg-black/80');

fs.writeFileSync('src/app/page.tsx', code);
