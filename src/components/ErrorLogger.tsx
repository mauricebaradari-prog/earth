'use client';
import { useEffect, useState } from 'react';

export default function ErrorLogger() {
  const [errors, setErrors] = useState<string[]>([]);

  useEffect(() => {
    const handleError = (e: ErrorEvent) => {
      setErrors(prev => [...prev, "Error: " + e.message + " at " + e.filename + ":" + e.lineno]);
    };
    const handleRejection = (e: PromiseRejectionEvent) => {
      setErrors(prev => [...prev, "Promise Rejection: " + String(e.reason)]);
    };

    window.addEventListener('error', handleError);
    window.addEventListener('unhandledrejection', handleRejection);

    return () => {
      window.removeEventListener('error', handleError);
      window.removeEventListener('unhandledrejection', handleRejection);
    };
  }, []);

  if (errors.length === 0) return null;

  return (
    <div style={{ position: 'absolute', top: 0, left: 0, right: 0, background: 'rgba(255,0,0,0.8)', color: 'white', padding: 10, zIndex: 99999, fontSize: 12, maxHeight: '30vh', overflow: 'auto' }}>
      <strong>Errors:</strong>
      <ul>
        {errors.map((err, i) => <li key={i}>{err}</li>)}
      </ul>
      <button onClick={() => setErrors([])} style={{ background: 'black', padding: '4px 8px', marginTop: 8 }}>Clear</button>
    </div>
  );
}
