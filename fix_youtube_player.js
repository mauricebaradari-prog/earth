const fs = require('fs');
let code = fs.readFileSync('src/components/YouTubeOverlay.tsx', 'utf8');

// 1. Add setIsReady(false) to cleanup
code = code.replace(
  `playerRef.current.destroy();\n        playerRef.current = null;`,
  `playerRef.current.destroy();\n        playerRef.current = null;\n        setIsReady(false);`
);

// 2. Add optional chaining to playVideo and pauseVideo in the useEffect
code = code.replace(
  `if (state.isAnimating) {\n      playerRef.current.playVideo();\n    } else {\n      const playerState = playerRef.current.getPlayerState ? playerRef.current.getPlayerState() : -1;\n      if (playerState !== -1 && playerState !== 5) {\n        playerRef.current.pauseVideo();\n      }`,
  `if (state.isAnimating) {\n      if (typeof playerRef.current.playVideo === 'function') playerRef.current.playVideo();\n    } else {\n      const playerState = typeof playerRef.current.getPlayerState === 'function' ? playerRef.current.getPlayerState() : -1;\n      if (playerState !== -1 && playerState !== 5) {\n        if (typeof playerRef.current.pauseVideo === 'function') playerRef.current.pauseVideo();\n      }`
);

// 3. Add optional chaining to the top-left-play-btn handler
code = code.replace(
  `if (!state.isAnimating && playerRef.current) {\n          playerRef.current.playVideo();\n        } else if (state.isAnimating && playerRef.current) {\n          playerRef.current.pauseVideo();\n        }`,
  `if (!state.isAnimating && playerRef.current && typeof playerRef.current.playVideo === 'function') {\n          playerRef.current.playVideo();\n        } else if (state.isAnimating && playerRef.current && typeof playerRef.current.pauseVideo === 'function') {\n          playerRef.current.pauseVideo();\n        }`
);

fs.writeFileSync('src/components/YouTubeOverlay.tsx', code);
