with open('src/components/GlobeMap.tsx', 'r') as f:
    text = f.read()

def check(open_char, close_char):
    count = 0
    lines = text.split('\n')
    for i, line in enumerate(lines):
        for char in line:
            if char == open_char: count += 1
            elif char == close_char: count -= 1
        if count < 0:
            print(f"Extra {close_char} on line {i+1}")
            count = 0
    print(f"Final count for {open_char}{close_char}: {count}")

check('(', ')')
check('{', '}')
check('[', ']')
check('<', '>')
