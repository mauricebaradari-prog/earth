const fs = require('fs');
let code = fs.readFileSync('src/components/YouTubeOverlay.tsx', 'utf8');

const findEffect = `    if (state.isAnimating && !lastAnimState.current) {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "playVideo",
        args: []
      }), '*');
    } else if (!state.isAnimating && lastAnimState.current) {
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
    } else {
      iframeRef.current.contentWindow.postMessage(JSON.stringify({
        event: "command",
        func: "pauseVideo",
        args: []
      }), '*');
    }`;

code = code.replace(findEffect, replaceEffect);
fs.writeFileSync('src/components/YouTubeOverlay.tsx', code);
