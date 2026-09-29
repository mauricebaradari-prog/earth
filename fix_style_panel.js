const fs = require('fs');
let code = fs.readFileSync('src/components/panels/StylePanel.tsx', 'utf8');

// The section is enclosed by {/* Map Style */} and {/* Route Color */}
code = code.replace(/\{\/\* Map Style \*\/\}[\s\S]*?\{\/\* Route Color \*\/\}/, '{/* Route Color */}');

fs.writeFileSync('src/components/panels/StylePanel.tsx', code);
