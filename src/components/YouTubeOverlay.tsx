import React, { useEffect, useRef, useState } from 'react';
import { useEditorState } from '../hooks/useEditorState';
import { Rnd } from 'react-rnd';
import { GripHorizontal } from 'lucide-react';

export default function YouTubeOverlay({ state, startAnimation, stopAnimation, initialPos, setActiveWindow }: any) {
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const playerRef = useRef<any>(null);
  const [isReady, setIsReady] = useState(false);
  const isInternalChange = useRef(false);
  const hasInitialized = useRef(false);
  const currentVideoIdRef = useRef<string>(state.videoId || '5EgtgRoC8NI');

  const [pos, setPos] = useState({ 
    x: typeof window !== 'undefined' ? window.innerWidth - 360 : 400, 
    y: 40 
  });
  const [size, setSize] = useState({ width: 320, height: 218 });
  const hasSetInitial = useRef(false);
  const [isPositioned, setIsPositioned] = useState(false);
  const [videoTitle, setVideoTitle] = useState("YOUTUBE VIDEO");

  useEffect(() => {
    if (initialPos && !hasSetInitial.current) {
      setPos(initialPos);
      hasSetInitial.current = true;
      // Small delay to ensure the position is applied before fading in
      setTimeout(() => setIsPositioned(true), 100);
    }
  }, [initialPos]);

  useEffect(() => {
    const initPlayer = () => {
      if (playerRef.current) return;
      playerRef.current = new (window as any).YT.Player('youtube-player', {
        videoId: currentVideoIdRef.current,
        playerVars: {
          autoplay: 0,
          controls: 0,
          modestbranding: 1,
          disablekb: 1,
          rel: 0,
          showinfo: 0,
          origin: 'http://localhost:3005',
          vq: isMobile ? 'hd1080' : undefined
        },
        events: {
          'onReady': () => { 
            setIsReady(true); 
            (window as any).__YT_PLAYER = playerRef.current; 
            try {
              if (isMobile && playerRef.current.setPlaybackQuality) {
                 playerRef.current.setPlaybackQuality('hd1080');
              }
              const data = playerRef.current.getVideoData();
              if (data && data.title) {
                setVideoTitle(data.title);
              }
            } catch(e) {}
          },
          'onStateChange': (event: any) => {
            try {
              if (isMobile && event.data === 1 && playerRef.current.setPlaybackQuality) {
                 playerRef.current.setPlaybackQuality('hd1080');
              }
            } catch(e) {}
            
            if (isInternalChange.current || (window as any).__IS_SCRUBBING) return;
            const isPlaying = event.data === 1;
            const isPaused = event.data === 2;
            const isBuffering = event.data === 3;
            const currentState = (window as any).__EDITOR_STATE;
            
            if (isPlaying && !currentState.isAnimating) {
              if (!(window as any).__yt_throttle_play) {
                (window as any).__yt_throttle_play = setTimeout(() => {
                  startAnimation();
                  (window as any).__yt_throttle_play = null;
                }, 100);
              }
            } else if ((isPaused || isBuffering) && currentState.isAnimating) {
              if (!(window as any).__yt_throttle_pause) {
                (window as any).__yt_throttle_pause = setTimeout(() => {
                  stopAnimation();
                  (window as any).__yt_throttle_pause = null;
                }, 100);
              }
            }
          }
        }
      });
    };

    if (!(window as any).YT) {
      const tag = document.createElement('script');
      tag.src = "https://www.youtube.com/iframe_api";
      const firstScriptTag = document.getElementsByTagName('script')[0];
      firstScriptTag.parentNode?.insertBefore(tag, firstScriptTag);
      (window as any).onYouTubeIframeAPIReady = initPlayer;
    } else if ((window as any).YT && (window as any).YT.Player) {
      initPlayer();
    }

    return () => {
      if (playerRef.current) {
        playerRef.current.destroy();
        playerRef.current = null;
        setIsReady(false);
      }
    };
  }, [startAnimation, stopAnimation]);

  // ── Switch video when route changes ──
  useEffect(() => {
    const newVideoId = state.videoId;
    if (!newVideoId || newVideoId === currentVideoIdRef.current) return;
    currentVideoIdRef.current = newVideoId;
    
    if (playerRef.current && playerRef.current.loadVideoById) {
      isInternalChange.current = true;
      playerRef.current.loadVideoById(newVideoId, 0);
      // Wait for the new video to be ready, then update the title
      setTimeout(() => {
        try {
          const data = playerRef.current.getVideoData();
          if (data && data.title) {
            setVideoTitle(data.title);
          }
        } catch(e) {}
        // Pause it so it doesn't autoplay, but only if we are not animating!
        const currentState = (window as any).__EDITOR_STATE;
        if (!currentState?.isAnimating) {
          try { playerRef.current.pauseVideo(); } catch(e) {}
        }
        isInternalChange.current = false;
      }, 1500);
    }
  }, [state.videoId]);

  useEffect(() => {
    (window as any).__EDITOR_STATE = state;
    
    const btn = document.getElementById('top-left-play-btn');
    if (btn) {
      const handler = () => {
        if (!state.isAnimating && playerRef.current && typeof playerRef.current.playVideo === 'function') {
          playerRef.current.playVideo();
        } else if (state.isAnimating && playerRef.current && typeof playerRef.current.pauseVideo === 'function') {
          playerRef.current.pauseVideo();
        }
      };
      btn.addEventListener('click', handler);
      return () => btn.removeEventListener('click', handler);
    }
  }, [state]);

  useEffect(() => {
    if (!isReady || !playerRef.current) return;
    isInternalChange.current = true;
    if (state.isAnimating) {
      if (typeof playerRef.current.playVideo === 'function') playerRef.current.playVideo();
    } else {
      const playerState = typeof playerRef.current.getPlayerState === 'function' ? playerRef.current.getPlayerState() : -1;
      if (playerState !== -1 && playerState !== 5) {
        if (typeof playerRef.current.pauseVideo === 'function') playerRef.current.pauseVideo();
      }
    }
    setTimeout(() => { isInternalChange.current = false; }, 200);
  }, [state.isAnimating, isReady]);

  const lastProgress = useRef(state.animationProgress);
  useEffect(() => {
    if (!isReady || !playerRef.current) return;
    if (state.animationProgress === 0 && lastProgress.current === 0) return;
    
    // Check if progress jumped significantly (e.g., a manual seek)
    const isManualSeek = Math.abs(state.animationProgress - lastProgress.current) > 0.005;
    
    if (isManualSeek || !state.isAnimating) {
      if (state.animationProgress !== lastProgress.current) {
        const targetTime = state.animationProgress * (state.durationSeconds || 2056);
        playerRef.current.seekTo(targetTime, true);
        lastProgress.current = state.animationProgress;
      }
    } else {
      // Natural progression while playing, just update lastProgress so we don't seek next time
      lastProgress.current = state.animationProgress;
    }
  }, [state.animationProgress, isReady, state.isAnimating]);

  useEffect(() => {
    if (playerRef.current && playerRef.current.setPlaybackRate) {
      playerRef.current.setPlaybackRate(state.animSpeed);
    }
  }, [state.animSpeed]);

  const [isMobile, setIsMobile] = useState(false);
  useEffect(() => {
    const handleResize = () => setIsMobile(window.innerWidth < 768);
    handleResize();
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const headerContent = (
    <div className="drag-handle w-full flex items-center justify-between cursor-move text-white/50 hover:text-white/90 transition-colors px-3" style={{ height: '38px', minHeight: '38px', flexShrink: 0 }}>
      <div className="flex flex-col justify-center overflow-hidden mr-2 pointer-events-none select-none h-full pt-0.5">
        <span className="text-white text-[11px] font-bold tracking-wide uppercase opacity-80 truncate">
          {videoTitle}
        </span>
        <span className="text-[#CCFF00]/80 text-[8px] tracking-wider uppercase font-medium truncate mt-[-1px]">
          *Video might not be 100% synced with route
        </span>
      </div>
      {!isMobile && <GripHorizontal size={20} className="shrink-0" />}
    </div>
  );

  const videoContent = (
    <div className="w-full relative bg-black" style={{ height: isMobile ? '100%' : 'calc(100% - 38px)' }}>
      <div id="youtube-player" className="absolute inset-0 w-full h-full"></div>
    </div>
  );

  if (isMobile) {
    return (
      <div 
        className="absolute left-0 w-full bg-black z-50 border-t border-b border-white/10" 
        style={{ top: '40vh', height: '35vh' }}
      >
        {videoContent}
      </div>
    );
  }

  return (
    <Rnd
      position={{ x: pos.x, y: pos.y }}
      size={{ width: size.width, height: size.height }}
      onDragStop={(e, d) => setPos({ x: d.x, y: d.y })}
      onResizeStop={(e, direction, ref, delta, position) => {
        setSize({ width: parseInt(ref.style.width), height: parseInt(ref.style.height) });
        setPos(position);
      }}
      minWidth={200}
      minHeight={150}
      lockAspectRatio={16/9}
      lockAspectRatioExtraHeight={38}
      bounds="parent"
      dragHandleClassName="drag-handle"
      className={`rounded-xl overflow-hidden shadow-[0_25px_50px_-12px_rgba(0,0,0,0.8),0_0_30px_rgba(0,0,0,0.5)] border border-white/20 bg-black/60 backdrop-blur-md flex flex-col transition-opacity duration-1000 ${isPositioned ? 'opacity-100' : 'opacity-0 pointer-events-none'}`}
      style={{ zIndex: state.activeWindow === 'video' ? 60 : 50 }}
      onDragStart={() => setActiveWindow && setActiveWindow('video')}
      onMouseDown={() => setActiveWindow && setActiveWindow('video')}
    >
      {headerContent}
      {videoContent}
    </Rnd>
  );
}
