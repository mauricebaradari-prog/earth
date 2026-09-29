import re

with open('src/components/YouTubeOverlay.tsx', 'r') as f:
    content = f.read()

# 1. Update the lockAspectRatioExtraHeight from 24 to 38
content = content.replace("lockAspectRatioExtraHeight={24}", "lockAspectRatioExtraHeight={38}")

# 2. Update the drag-handle height and inner content
old_handle = """      <div className="drag-handle w-full flex items-center justify-between cursor-move text-white/50 hover:text-white/90 transition-colors px-3" style={{ height: '24px', minHeight: '24px', flexShrink: 0 }}>
        <span className="text-white text-[11px] font-bold tracking-wide uppercase opacity-80 truncate mr-2 pointer-events-none select-none">
          {videoTitle}
        </span>
        <GripHorizontal size={20} className="shrink-0" />
      </div>
      {/* Container for the iframe to maintain exact 16:9 inner ratio */}
      <div className="w-full relative bg-black" style={{ height: 'calc(100% - 24px)' }}>"""

new_handle = """      <div className="drag-handle w-full flex items-center justify-between cursor-move text-white/50 hover:text-white/90 transition-colors px-3" style={{ height: '38px', minHeight: '38px', flexShrink: 0 }}>
        <div className="flex flex-col justify-center overflow-hidden mr-2 pointer-events-none select-none h-full pt-0.5">
          <span className="text-white text-[11px] font-bold tracking-wide uppercase opacity-80 truncate">
            {videoTitle}
          </span>
          <span className="text-[#CCFF00]/80 text-[8px] tracking-wider uppercase font-medium truncate mt-[-1px]">
            *Video might not be 100% synced with route
          </span>
        </div>
        <GripHorizontal size={20} className="shrink-0" />
      </div>
      {/* Container for the iframe to maintain exact 16:9 inner ratio */}
      <div className="w-full relative bg-black" style={{ height: 'calc(100% - 38px)' }}>"""

content = content.replace(old_handle, new_handle)

with open('src/components/YouTubeOverlay.tsx', 'w') as f:
    f.write(content)
