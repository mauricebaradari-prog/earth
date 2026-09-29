import re

with open('src/hooks/useEditorState.ts', 'r') as f:
    content = f.read()

old_start = """  const startAnimation = useCallback(() => {
    setState((prev) => {"""

new_start = """  const startAnimation = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    setState((prev) => {"""

content = content.replace(old_start, new_start)

old_stop = """  const stopAnimation = useCallback(() => {
    if (rafRef.current) cancelAnimationFrame(rafRef.current);
    setState((prev) => ({ ...prev, isAnimating: false }));
  }, []);"""

new_stop = """  const stopAnimation = useCallback(() => {
    if (rafRef.current) {
      cancelAnimationFrame(rafRef.current);
      rafRef.current = null;
    }
    setState((prev) => ({ ...prev, isAnimating: false }));
  }, []);"""

content = content.replace(old_stop, new_stop)

with open('src/hooks/useEditorState.ts', 'w') as f:
    f.write(content)
