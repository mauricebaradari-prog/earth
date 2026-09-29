const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

// The easiest way is to add a new import statement below it
if (!code.includes("import { Video } from 'lucide-react';")) {
  code = code.replace(
    `} from 'lucide-react';`,
    `} from 'lucide-react';\nimport { Video } from 'lucide-react';`
  );
  fs.writeFileSync('src/app/page.tsx', code);
}
