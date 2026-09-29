with open('src/components/GlobeMap.tsx', 'r') as f:
    text = f.read()

def find_unclosed(open_char, close_char):
    stack = []
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for j, char in enumerate(line):
            if char == open_char:
                stack.append((i+1, j+1))
            elif char == close_char:
                if stack:
                    stack.pop()
    print(f"Unclosed {open_char}: {stack}")

find_unclosed('(', ')')
find_unclosed('{', '}')
