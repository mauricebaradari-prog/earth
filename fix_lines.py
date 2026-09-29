import re
with open('src/components/GlobeMap.tsx', 'r') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 231:
        new_lines.append("  }\n")
    elif i == 232 or i == 233:
        continue
    else:
        new_lines.append(line)

with open('src/components/GlobeMap.tsx', 'w') as f:
    f.writelines(new_lines)
