const fs = require('fs');
let code = fs.readFileSync('src/hooks/useEditorState.ts', 'utf8');

const findSet = `    set: (key: keyof EditorState, value: any) =>
      setState((prev) => ({ ...prev, [key]: value })),`;

const replaceSet = `    set: (key: keyof EditorState, value: any) =>
      setState((prev) => {
        if (key === 'animSpeed' && value > 2) value = 2;
        return { ...prev, [key]: value };
      }),`;

code = code.replace(findSet, replaceSet);
fs.writeFileSync('src/hooks/useEditorState.ts', code);
