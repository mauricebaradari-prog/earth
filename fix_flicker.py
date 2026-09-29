import re

with open('src/components/GlobeMap.tsx', 'r') as f:
    content = f.read()

# Replace the inner marker building logic
old_logic = """      // Create DOM element for the marker
      const el = document.createElement('div');
      el.className = 'route-preview-marker relative group cursor-pointer transition-transform hover:scale-110 hover:z-50';
      el.style.width = '90px';
      el.style.height = '60px';
      el.style.borderRadius = '8px';
      el.style.overflow = 'hidden';
      el.style.border = '2px solid rgba(255, 255, 255, 0.4)';
      el.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.5)';
      
      const img = document.createElement('img');
      img.src = route.videoId ? `https://img.youtube.com/vi/${route.videoId}/mqdefault.jpg` : 'https://images.unsplash.com/photo-1542281286-9e0a16bb7366?auto=format&fit=crop&w=300&q=80';
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.objectFit = 'cover';
      el.appendChild(img);

      // Play icon overlay
      const overlay = document.createElement('div');
      overlay.className = 'absolute inset-0 bg-black/40 flex items-center justify-center opacity-70 group-hover:opacity-100 transition-opacity';
      overlay.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
      el.appendChild(overlay);
      
      // Title overlay
      const title = document.createElement('div');
      title.className = 'absolute bottom-0 w-full bg-black/70 text-white text-[9px] font-bold px-1 py-0.5 truncate text-center';
      title.innerText = route.name || 'Route';
      el.appendChild(title);"""

new_logic = """      // Create DOM element for the marker container (MUST NOT be transformed by CSS hover)
      const el = document.createElement('div');
      el.className = 'route-preview-marker-container cursor-pointer';
      
      // Create inner element that handles the hover effects safely
      const inner = document.createElement('div');
      inner.className = 'relative group transition-transform hover:scale-110 hover:z-50';
      inner.style.width = '90px';
      inner.style.height = '60px';
      inner.style.borderRadius = '8px';
      inner.style.overflow = 'hidden';
      inner.style.border = '2px solid rgba(255, 255, 255, 0.4)';
      inner.style.boxShadow = '0 10px 25px -5px rgba(0, 0, 0, 0.5)';
      
      const img = document.createElement('img');
      img.src = route.videoId ? `https://img.youtube.com/vi/${route.videoId}/mqdefault.jpg` : 'https://images.unsplash.com/photo-1542281286-9e0a16bb7366?auto=format&fit=crop&w=300&q=80';
      img.style.width = '100%';
      img.style.height = '100%';
      img.style.objectFit = 'cover';
      inner.appendChild(img);

      // Play icon overlay
      const overlay = document.createElement('div');
      overlay.className = 'absolute inset-0 bg-black/40 flex items-center justify-center opacity-70 group-hover:opacity-100 transition-opacity';
      overlay.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="white" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="5 3 19 12 5 21 5 3"></polygon></svg>`;
      inner.appendChild(overlay);
      
      // Title overlay
      const title = document.createElement('div');
      title.className = 'absolute bottom-0 w-full bg-black/70 text-white text-[9px] font-bold px-1 py-0.5 truncate text-center';
      title.innerText = route.name || 'Route';
      inner.appendChild(title);
      
      el.appendChild(inner);"""

content = content.replace(old_logic, new_logic)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.write(content)
