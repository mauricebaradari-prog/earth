import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

elev_ui = """          <div className="w-full h-full bg-black/80 backdrop-blur-md p-4 rounded-xl border border-white/10 shadow-2xl flex flex-col cursor-grab active:cursor-grabbing">
            <div className="flex justify-between items-center mb-2 pointer-events-none">
              <span className="text-white text-[11px] font-bold tracking-widest uppercase opacity-90">Elevation Profile</span>
              <button className="text-white/50 hover:text-white pointer-events-auto p-1">
                <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M5 12h14"/></svg>
              </button>
            </div>
            <div className="flex gap-2 text-[11px] text-white/50 mb-3 pointer-events-none">
              <span>{Math.round(totalDistRef.current)} KM</span>
              <span>·</span>
              <span>{Math.floor(durationSeconds/60)}M {durationSeconds%60}S</span>
            </div>
            
            <div className="relative w-full flex-1 pointer-events-auto cursor-pointer" onClick={(e) => {
                if (!onSeek) return;
                const rect = e.currentTarget.getBoundingClientRect();
                let p = (e.clientX - rect.left) / rect.width;
                p = Math.max(0, Math.min(1, p));
                onSeek(p);
            }}>
              {/* Grid Lines */}
              <div className="absolute inset-0 flex flex-col justify-between pointer-events-none">
                <div className="w-full h-px border-t border-white/10 border-dashed"></div>
                <div className="w-full h-px border-t border-white/10 border-dashed"></div>
                <div className="w-full h-px border-t border-white/10 border-dashed"></div>
              </div>
              {/* Y Axis Labels */}
              <div className="absolute left-0 top-0 bottom-0 flex flex-col justify-between text-[9px] text-white/40 pr-2 pointer-events-none">
                <span>{Math.round(Math.max(...(elevationProfile || [0])))}m</span>
                <span>{Math.round(Math.min(...(elevationProfile || [0])))}m</span>
              </div>
              
              <svg width="100%" height="100%" viewBox="0 0 368 70" preserveAspectRatio="none">"""

content = re.sub(
    r'<div className="w-full h-full bg-black/60 backdrop-blur-md p-4 rounded-xl border border-white/10 shadow-2xl flex flex-col gap-2 cursor-grab active:cursor-grabbing">.*?<svg width="100%" height="100%" viewBox="0 0 368 70" preserveAspectRatio="none">',
    elev_ui,
    content,
    flags=re.DOTALL
)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
