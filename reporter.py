#!/usr/bin/env python3

from typing import Dict

topic: Dict[str, int] = {}

with open('index.Rmd') as f:
    for line in f:
        if line.startswith("##"):
            name: str = line[3:len(line) - 1]
            topic[name], counter = 0, 0
        elif line.startswith("*"):
            topic[name] += 1

topic_sorted = {
    k: v
    for k, v in sorted(topic.items(), key=lambda item: item[1], reverse=True)
}

for name in topic_sorted:
    number: int = int(topic[name])
    links: str = "links" if number > 1 else "link"
    print(f"{name}:\n  {number} {links}")
