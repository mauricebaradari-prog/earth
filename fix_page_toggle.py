import re
with open('src/app/page.tsx', 'r') as f:
    content = f.read()

# Add state
content = content.replace("  const [showElevation, setShowElevation] = useState(true);", "  const [showElevation, setShowElevation] = useState(true);\n  const [useGpsTrace, setUseGpsTrace] = useState(false);")

# Pass to GlobeMap
content = content.replace("              showElevation={showElevation}", "              showElevation={showElevation}\n              useGpsTrace={useGpsTrace}")

# Add button
button_code = """      {/* ── Top Right Elevation Toggle ── */}
      <div className="absolute top-6 right-6 z-50 flex gap-2">
        <button
          onClick={() => setUseGpsTrace(!useGpsTrace)}
          className={`px-4 h-10 rounded-full flex items-center justify-center backdrop-blur-md transition-all border ${
            useGpsTrace 
              ? 'bg-lime-400 text-black border-lime-400 shadow-[0_0_15px_rgba(204,255,0,0.4)]' 
              : 'bg-black/50 text-white/70 border-white/10 hover:bg-black/70 hover:text-white'
          }`}
          title="Toggle GPS Trace Test"
        >
          <span className="text-xs font-bold uppercase tracking-wider">GPS Test</span>
        </button>"""

content = re.sub(
    r'      \{\/\* ── Top Right Elevation Toggle ── \*\/\}\n      <div className="absolute top-6 right-6 z-50">',
    button_code,
    content
)

with open('src/app/page.tsx', 'w') as f:
    f.write(content)
