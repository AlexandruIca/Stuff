#!/usr/bin/env python

from typing import List

def capitalize_word(text: str) -> str:
    common: List[str] = [
        "for", "to", "in", "on", "a", "an", "with", "from", "the", "of", "and"
    ]

    if len(text) == 0 or text.isupper():
        return text

    if text.lower() not in common:
        return text[0].upper() + text[1:]
    else:
        return text.lower()

def capitalize(text: str) -> str:
    return ' '.join([capitalize_word(x) for x in text.split()])

with open('index.md') as f:
    for line in f:
        if line.startswith("* ["):
            started: bool = False
            tmp: str = ""
            rest: str = ""

            for char in line:
                if char == '[':
                    started = True
                elif char == ']':
                    started = False
                    rest = ']'
                elif started == True:
                    tmp += char
                elif started == False:
                    rest += char

            print(f"* [{capitalize(tmp)}" + rest, end='')
        else:
            print(line, end='')
