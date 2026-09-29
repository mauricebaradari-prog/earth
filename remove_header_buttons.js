const fs = require('fs');
let code = fs.readFileSync('src/app/page.tsx', 'utf8');

const findButtons = `            <a
              href="https://buymeacoffee.com"
              target="_blank"
              rel="noopener noreferrer"
              className="p-1.5 rounded-full bg-[#FFDD00]/10 hover:bg-[#FFDD00]/20 text-[#FFDD00] transition-all"
              title="Support the project"
            >
              <Coffee className="w-3.5 h-3.5" />
            </a>
            <button
              disabled
              className="p-1.5 rounded-full bg-gray-800 text-gray-600 cursor-not-allowed hidden md:block"
              title="Share Route"
            >
              <Share2 className="w-3.5 h-3.5" />
            </button>`;

code = code.replace(findButtons, '');
fs.writeFileSync('src/app/page.tsx', code);
