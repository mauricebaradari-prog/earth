const fs = require('fs');
let code = fs.readFileSync('src/components/YouTubeOverlay.tsx', 'utf8');

const findEffect = `    if (state.isAnimating) {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "playVideo",
        args: []
      }), '*');
    } else {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "pauseVideo",
        args: []
      }), '*');
    }`;

const replaceEffect = `    if (state.isAnimating) {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "playVideo",
        args: []
      }), '*');
      // Fallback in case iframe was still booting up
      setTimeout(() => {
        if (iframeRef.current && iframeRef.current.contentWindow) {
          iframeRef.current.contentWindow.postMessage(JSON.stringify({
            event: "command",
            func: "playVideo",
            args: []
          }), '*');
        }
      }, 1500);
    } else {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "pauseVideo",
        args: []
      }), '*');
    }`;

code = code.replace(findEffect, replaceEffect);
fs.writeFileSync('src/components/YouTubeOverlay.tsx', code);
