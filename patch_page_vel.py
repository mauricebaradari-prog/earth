import re

with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# Add Gauge to lucide-react imports
content = re.sub(
    r'import \{ (.*?) \} from \'lucide-react\';',
    r"import { \1, Gauge } from 'lucide-react';",
    content
)

# Add showVelocity state
content = re.sub(
    r'const \[showElevation, setShowElevation\] = useState\(true\);',
    r"const [showElevation, setShowElevation] = useState(true);\n  const [showVelocity, setShowVelocity] = useState(true);",
    content
)

# Add Velocity toggle button next to Elevation
old_elev_btn = """            <button 
              onClick={() => setShowElevation(!showElevation)}
              className={`p-2 rounded hover:bg-white/10 transition-colors ${showElevation ? 'text-[#CCFF00]' : 'text-gray-400'}`}
              title="Toggle Elevation"
            >
              <Mountain size={20} />
            </button>"""

new_elev_btn = """            <button 
              onClick={() => setShowElevation(!showElevation)}
              className={`p-2 rounded hover:bg-white/10 transition-colors ${showElevation ? 'text-[#CCFF00]' : 'text-gray-400'}`}
              title="Toggle Elevation"
            >
              <Mountain size={20} />
            </button>
            <button 
              onClick={() => setShowVelocity(!showVelocity)}
              className={`p-2 rounded hover:bg-white/10 transition-colors ${showVelocity ? 'text-[#CCFF00]' : 'text-gray-400'}`}
              title="Toggle Velocity"
            >
              <Gauge size={20} />
            </button>"""

content = content.replace(old_elev_btn, new_elev_btn)

# Pass showVelocity to GlobeMap
content = re.sub(
    r'showElevation=\{showElevation\}',
    r'showElevation={showElevation}\n          showVelocity={showVelocity}',
    content
)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
