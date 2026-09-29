const fs = require('fs');
let code = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

const findJSX = `<div className="absolute inset-0 bg-[#04071200]">
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />`;
      
const replaceJSX = `<div className="absolute inset-0 bg-[#04071200]">
      <div ref={containerRef} style={{ width: '100%', height: '100%' }} />
      <div style={{ position: 'absolute', top: '10px', left: '10px', background: 'rgba(0,0,0,0.8)', color: '#0f0', padding: '10px', zIndex: 9999, fontFamily: 'monospace', fontSize: '14px', borderRadius: '8px', border: '1px solid #0f0' }}>
        <strong>DEBUG INFO (Please screenshot this):</strong><br/>
        isAnimating: {isAnimating ? 'YES' : 'NO'}<br/>
        Progress: {Math.round(animationProgress * 100)}%<br/>
        SVG Path length: {svgPath.length}<br/>
        Full Path length: {fullSvgPath.length}<br/>
        Cities: {cities.length}<br/>
        Route Pass: {renderPassRef.current}
      </div>`;

code = code.replace(findJSX, replaceJSX);
fs.writeFileSync('src/components/GlobeMap.tsx', code);
