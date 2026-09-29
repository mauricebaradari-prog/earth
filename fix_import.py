import re
with open('src/app/page.tsx', 'r') as f:
    content = f.read()

if "import sparklinesData from" not in content:
    content = content.replace("import React, { useState }", "import sparklinesData from '../data/sparklines.json';\nimport React, { useState }")

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
