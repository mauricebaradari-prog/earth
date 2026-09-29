import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

old_tick = """    const tick = (now: number) => {
      if (lastTimeRef.current === null) lastTimeRef.current = now;
      const dt = (now - lastTimeRef.current) / 1000;
      lastTimeRef.current = now;

      setState((prev) => {
        if (!prev.isAnimating) return prev;
        const speed = prev.animSpeed / (prev.durationSeconds || 2056); // progress units per second
        const next = prev.animationProgress + dt * speed;
        if (next >= 1) {
          return { ...prev, animationProgress: 1, isAnimating: false };
        }
        return { ...prev, animationProgress: next };
      });

      rafRef.current = requestAnimationFrame(tick);
    };"""

new_tick = """    const tick = (now: number) => {
      if (lastTimeRef.current === null) lastTimeRef.current = now;
      const dt = (now - lastTimeRef.current) / 1000;
      
      // Safety hatch: if dt is 0 or extremely small (e.g. synchronous call bug), ignore
      if (dt > 0.001) {
        lastTimeRef.current = now;
        setState((prev) => {
          if (!prev.isAnimating) return prev;
          const speed = prev.animSpeed / (prev.durationSeconds || 2056); // progress units per second
          const next = Math.min(1, prev.animationProgress + dt * speed);
          if (next >= 1) {
            return { ...prev, animationProgress: 1, isAnimating: false };
          }
          // Prevent React state thrashing if progress barely changed
          if (Math.abs(prev.animationProgress - next) < 0.0001) return prev;
          return { ...prev, animationProgress: next };
        });
      }

      rafRef.current = requestAnimationFrame(tick);
    };"""

content = content.replace(old_tick, new_tick)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
