#!/usr/bin/env python3

import sys

if len(sys.argv) != 4:
    print("-------ERROR-------")
    print("I need 3 arguments: start_line, end_line, tag")
    sys.exit(-1)

start_line: int = int(sys.argv[1])
end_line: int = int(sys.argv[2])
tag: str = sys.argv[3]

if start_line > end_line:
    print("-------ERROR-------")
    print("start_line > end_line")
    sys.exit(-1)

def process_line(line: str):
    inside_title: bool = False
    title: str = ''
    inside_link: str = ''
    link: str = ''
    inside_description: bool = False
    description: str = ''
    current_str: str = ''

    for ch in line:
        if ch == '[':
            inside_title = True
            continue
        elif ch == ']':
            inside_title = False
            title = current_str
            current_str = ''
            continue
        elif ch == '(':
            inside_link = True
            continue
        elif ch == ')':
            inside_link = False
            link = current_str
            current_str = ''
            inside_description = True
            continue
        
        if inside_title or inside_link or inside_description:
            current_str += ch
    
    description = current_str
    print(f'"{link}","{title}","{description[3:]}","{tag}"')

with open('../index.md', 'r') as f:
    line_num: int = 0

    for line in f:
        line_num += 1

        if start_line <= line_num <= end_line:
            process_line(line[:-1])