#!/usr/bin/env python

from typing import Dict

topic: Dict[str, int] = {}

with open('index.md') as f:
    line_no: int = 0

    for line in f:
        line_no += 1
        if line_no <= 51:
            continue

        if line.startswith("## "):
            name: str = line[3:len(line) - 1]
            topic[name], counter = 0, 0
        elif line.startswith("*"):
            topic[name] += 1

topic_sorted = {
    k: v
    for k, v in sorted(topic.items(), key=lambda item: item[1], reverse=True)
}

total: int = 0

for name in topic_sorted:
    number: int = int(topic[name])
    links: str = "links" if number > 1 else "link"

    print(f"{name}:\n  {number} {links}")
    total += number

print(f"\nTotal: {total} links")
