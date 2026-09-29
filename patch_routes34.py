import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

error_handler_patch = """
  const [globalErr, setGlobalErr] = React.useState<string | null>(null);
  
  useEffect(() => {
    const handleErr = (e: ErrorEvent) => setGlobalErr(e.message);
    const handleRej = (e: PromiseRejectionEvent) => setGlobalErr(e.reason?.toString());
    window.addEventListener('error', handleErr);
    window.addEventListener('unhandledrejection', handleRej);
    return () => {
      window.removeEventListener('error', handleErr);
      window.removeEventListener('unhandledrejection', handleRej);
    };
  }, []);

  // ── 1. Map Initialization ───────────────────────────────────────────────────"""

content = content.replace("  // ── 1. Map Initialization ───────────────────────────────────────────────────", error_handler_patch)

jsx_err_patch = """      {/* Debug Info */}
      {globalErr && (
        <div style={{ position: 'absolute', top: 50, left: 10, background: 'red', color: 'white', padding: '10px', zIndex: 10000, maxWidth: '80%' }}>
          FATAL ERROR: {globalErr}
        </div>
      )}
      <div style={{ position: 'absolute', bottom: 10, left: 10, background: 'rgba(0,0,0,0.8)', color: 'white', padding: '5px', zIndex: 9999, fontSize: '10px' }}>"""

content = content.replace("      {/* Debug Info */}\n      <div style={{ position: 'absolute', bottom: 10, left: 10, background: 'rgba(0,0,0,0.8)', color: 'white', padding: '5px', zIndex: 9999, fontSize: '10px' }}>", jsx_err_patch)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
