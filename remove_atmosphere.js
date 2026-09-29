const fs = require('fs');

// 1. Remove from useEditorState.ts
let codeState = fs.readFileSync('src/hooks/useEditorState.ts', 'utf8');
codeState = codeState.replace(/globeAtmosphere: boolean;\n/g, '');
codeState = codeState.replace(/globeAtmosphere: true,\n/g, '');
fs.writeFileSync('src/hooks/useEditorState.ts', codeState);

// 2. Remove from StylePanel.tsx
let codeStyle = fs.readFileSync('src/components/panels/StylePanel.tsx', 'utf8');
const findProps = `  globeAtmosphere: boolean;
  routeColor: string;
  routeWidth: number;
  onMapStyle: (s: MapStyleId) => void;
  onAtmosphere: (v: boolean) => void;
  onRouteColor: (c: string) => void;`;
const replaceProps = `  routeColor: string;
  routeWidth: number;
  onMapStyle: (s: MapStyleId) => void;
  onRouteColor: (c: string) => void;`;
codeStyle = codeStyle.replace(findProps, replaceProps);

const findDestruct = `  globeAtmosphere,
  routeColor,
  routeWidth,
  onMapStyle,
  onAtmosphere,
  onRouteColor,`;
const replaceDestruct = `  routeColor,
  routeWidth,
  onMapStyle,
  onRouteColor,`;
codeStyle = codeStyle.replace(findDestruct, replaceDestruct);

const findUI = `      {/* Atmosphere */}
      <div>
        <h3 className="text-[10px] font-bold text-gray-500 uppercase tracking-widest mb-2">
          Globe Atmosphere
        </h3>
        <label className="flex items-center justify-between rounded-xl bg-white/5 border border-white/5 px-4 py-3 cursor-pointer hover:border-white/10 transition-all">
          <div>
            <div className="text-sm font-medium text-white">Space glow</div>
            <div className="text-[10px] text-gray-500">Blue limb effect & star field</div>
          </div>
          <div
            onClick={() => onAtmosphere(!globeAtmosphere)}
            className={\`relative w-10 h-5.5 rounded-full transition-colors \${globeAtmosphere ? 'bg-yellow-400' : 'bg-gray-700'}\`}
            style={{ width: '40px', height: '22px' }}
          >
            <div
              className={\`absolute top-0.5 w-4.5 h-4.5 bg-white rounded-full shadow transition-transform \${globeAtmosphere ? 'translate-x-5' : 'translate-x-0.5'}\`}
              style={{ width: '18px', height: '18px', transform: globeAtmosphere ? 'translateX(20px)' : 'translateX(2px)' }}
            />
          </div>
        </label>
      </div>`;
codeStyle = codeStyle.replace(findUI, '');
fs.writeFileSync('src/components/panels/StylePanel.tsx', codeStyle);

// 3. Remove from page.tsx
let codePage = fs.readFileSync('src/app/page.tsx', 'utf8');
const findPageProps = `              mapStyle={state.mapStyle}
              globeAtmosphere={state.globeAtmosphere}
              routeColor={state.routeColor}
              routeWidth={state.routeWidth}
              onMapStyle={(s) => set('mapStyle', s)}
              onAtmosphere={(a) => set('globeAtmosphere', a)}
              onRouteColor={(c) => set('routeColor', c)}`;
const replacePageProps = `              mapStyle={state.mapStyle}
              routeColor={state.routeColor}
              routeWidth={state.routeWidth}
              onMapStyle={(s) => set('mapStyle', s)}
              onRouteColor={(c) => set('routeColor', c)}`;
codePage = codePage.replace(findPageProps, replacePageProps);
const findGlobeProps = `          globeAtmosphere={state.globeAtmosphere}`;
codePage = codePage.replace(findGlobeProps, '');
fs.writeFileSync('src/app/page.tsx', codePage);

// 4. Remove from GlobeMap.tsx
let codeGlobe = fs.readFileSync('src/components/GlobeMap.tsx', 'utf8');
const findGlobeInterface = `interface GlobeMapProps {
  cities: City[];
  mapStyle: EditorState['mapStyle'];
  globeAtmosphere: boolean;
  animationProgress: number;`;
const replaceGlobeInterface = `interface GlobeMapProps {
  cities: City[];
  mapStyle: EditorState['mapStyle'];
  animationProgress: number;`;
codeGlobe = codeGlobe.replace(findGlobeInterface, replaceGlobeInterface);

const findGlobeDestruct = `  cities,
  mapStyle,
  globeAtmosphere,
  animationProgress,`;
const replaceGlobeDestruct = `  cities,
  mapStyle,
  animationProgress,`;
codeGlobe = codeGlobe.replace(findGlobeDestruct, replaceGlobeDestruct);

codeGlobe = codeGlobe.replace(/map\.setSky\(\{ 'atmosphere-blend': globeAtmosphere \? 1\.0 : 0\.0 \}\);\n/g, '');
codeGlobe = codeGlobe.replace(/      map\.setSky\(\{ 'atmosphere-blend': globeAtmosphere \? 1\.0 : 0\.0 \}\);\n/g, '');

fs.writeFileSync('src/components/GlobeMap.tsx', codeGlobe);
