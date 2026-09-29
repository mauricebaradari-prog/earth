import re

with open('src/components/YouTubeOverlay.tsx', 'r') as f:
    content = f.read()

old_state_change = """            if (isPlaying && !currentState.isAnimating) {
              startAnimation();
            } else if ((isPaused || isBuffering) && currentState.isAnimating) {
              stopAnimation();
            }"""

new_state_change = """            if (isPlaying && !currentState.isAnimating) {
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
            }"""

content = content.replace(old_state_change, new_state_change)

with open('src/components/YouTubeOverlay.tsx', 'w') as f:
    f.write(content)
