const fs = require('fs');
let code = fs.readFileSync('src/app/layout.tsx', 'utf8');

code = 'import ErrorLogger from "@/components/ErrorLogger";\n' + code;

fs.writeFileSync('src/app/layout.tsx', code);
