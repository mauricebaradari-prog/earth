const fs = require('fs');

let content = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');

// 1. Change containerRef to have 40vh on mobile
content = content.replace(
  /<div className="w-full h-full relative" ref={containerRef}>/g,
  '<div className="w-full h-full relative pointer-events-none z-0"><div className="w-full relative pointer-events-auto" style={{ height: isMobile ? "40vh" : "100%" }} ref={containerRef}>'
);

// We must also close this new parent div at the very end of GlobeMap return statement.
// The return statement ends around line 1332. 
// Let's find the end of GlobeMap.
const closeDivStr = `        </Rnd>
      )}
    </div>
  );
}`;

const closeDivReplacement = `        </Rnd>
      )}
    </div>
    </div>
  );
}`;
content = content.replace(closeDivStr, closeDivReplacement);

// 2. Wrap ElevationProfile logic
const elevRndStart = `{showElevation && elevationProfile && (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 24, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'elevation' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('elevation')}
          onMouseDown={() => setActiveWindow && setActiveWindow('elevation')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">`;

const elevRndReplacement = `{showElevation && elevationProfile && (
        isMobile ? (
          <div className="absolute left-0 w-full bg-black/90 backdrop-blur-md flex flex-col z-50 pointer-events-auto" style={{ top: '75vh', height: '25vh' }}>
            <div style={{ width: '100%', height: '100%', padding: '16px', display: 'flex', flexDirection: 'column' }}>
        ) : (
        <Rnd
          default={{ x: typeof window !== 'undefined' ? window.innerWidth - 344 : 0, y: 24, width: 320, height: 'auto' }}
          bounds="parent"
          enableResizing={false}
          className="z-50"
          style={{ zIndex: activeWindow === 'elevation' ? 60 : 50 }}
          onDragStart={() => setActiveWindow && setActiveWindow('elevation')}
          onMouseDown={() => setActiveWindow && setActiveWindow('elevation')}
        >
        <div style={{ width: '100%', height: '100%', background: 'linear-gradient(180deg, rgba(17,17,17,0.6) 0%, rgba(17,17,17,0.4) 100%)', borderRadius: '12px', border: '1px solid rgba(255,255,255,0.08)', padding: '16px', backdropFilter: 'blur(12px)', boxShadow: '0 8px 32px rgba(0,0,0,0.4)', pointerEvents: 'auto', cursor: 'grab' }} className="active:cursor-grabbing">
        )
      )}`;

content = content.replace(elevRndStart, elevRndStart.replace('<Rnd', 'isMobile ? (\n<div className="absolute left-0 w-full pointer-events-auto bg-black/90 backdrop-blur-md z-50 flex flex-col" style={{ top: "75vh", height: "25vh" }}>\n<div style={{ padding: "16px", height: "100%", width: "100%", display: "flex", flexDirection: "column" }}>\n) : (\n<Rnd').replace('className="active:cursor-grabbing">', 'className="active:cursor-grabbing">\n)'));

fs.writeFileSync('src/components/GlobeMap.tsx', content);
