const fs = require('fs');
let code = fs.readFileSync('src/components/YouTubeOverlay.tsx', 'utf8');

code = code.replace(
  `dragHandleClassName="drag-handle"\n      className={\`z-50 rounded-xl overflow-hidden shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8),0_0_30px_rgba(0,0,0,0.5)] border border-white/20 bg-black/60 backdrop-blur-md flex flex-col transition-opacity duration-1000 \${isPositioned ? 'opacity-100' : 'opacity-0 pointer-events-none'}\`}`,
  `dragHandleClassName="drag-handle"\n      className={\`rounded-xl overflow-hidden shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8),0_0_30px_rgba(0,0,0,0.5)] border border-white/20 bg-black/60 backdrop-blur-md flex flex-col transition-opacity duration-1000 \${isPositioned ? 'opacity-100' : 'opacity-0 pointer-events-none'}\`}\n      style={{ zIndex: state.activeWindow === 'video' ? 60 : 50 }}\n      onDragStart={() => setActiveWindow && setActiveWindow('video')}\n      onMouseDown={() => setActiveWindow && setActiveWindow('video')}`
);

fs.writeFileSync('src/components/YouTubeOverlay.tsx', code);
