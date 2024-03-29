#!/usr/bin/env python3

from typing import Dict, List, Tuple

import sys
import csv

tag_mapping: Dict[str, int] = {
    'js': 0,
    'ts': 0,
    'javascript': 0,

    'graphics': 1,
    'graphics programming': 1,
    'graphics-programming': 1,

    'render graph': 2,
    'render-graph': 2,

    'game engine': 3,
    'game-engine': 3,

    'book': 4,

    'PBR': 5,
    'pbr': 5,
    'physically-based rendering': 5,
    'physically-based-rendering': 5,
    'physically based rendering': 5,

    'path-tracing': 6,
    'path tracing': 6,
    'path-tracer': 6,
    'path tracer': 6,

    'ray marching': 7,
    'ray-marching': 7,
    'ray-march': 7,
    'ray march': 7,
    'ray-marcher': 7,
    'ray marcher': 7,

    'global illumination': 8,
    'global-illumination': 8,

    'presentation': 9,
    'video': 9,
    'youtube': 9,

    'blog': 10,

    'course': 11,
    'lecture': 11,

    'opengl': 12,
    'OpenGL': 12,

    'algorithm': 13,
    'data-structure': 13,
    'data structure': 13,
    'paper': 13,

    'computational-geometry': 14,
    'computational geometry': 14,
    'geometry': 14,

    'resource-collection': 15,
    'resource collection': 15,
    'resources': 15,

    'tool': 16,
    'tooling': 16,
    'tools': 16,

    'tutorial': 17,
    'library': 18,

    'rust': 19,
    'Rust': 19,

    'cpp': 20,
    'c++': 20,
    'C++': 20,

    'physics': 21,
    'fluid-simulation': 22,

    'gui': 23,
    'GUI': 23,
    'UI': 23,

    'fun': 24,
    'funny': 24,

    'misc': 25,

    'off-topic': 26,
    'off topic': 26,

    'collision-detection': 27,
    'collision detection': 27,

    'project-ideas': 28,
    'project ideas': 28,
    'project-idea': 28,
    'project idea': 28,

    'cad': 29,
    'CAD': 29,

    'color-processing': 30,
    'color processing': 30,
    'color-theory': 30,
    'color theory': 30,
    'color-space': 30,
    'color space': 30,
    'color-spaces': 30,
    'color spaces': 30,

    'hardware': 31,
    'ascii-art': 32,

    'hdl': 33,
    'HDL': 33,
    'hardware-description-language': 33,
    'hardware description language': 33,
    'verilog': 33,
    'vhdl': 33,

    'c': 34,
    'C': 34,

    'gpgpu': 35,
    'GPGPU': 35,

    'vcs': 36,
    'VCS': 36,
    'version-control-system': 36,
    'version control system': 36,
    'git': 36,

    'programming-languages': 37,
    'programming languages': 37,
    'programming-language': 37,
    'programming language': 37,

    'compiler-theory': 38,
    'compiler theory': 38,
    'compilers': 38,
    'plt': 38,
    'PLT': 38,

    'python': 39,

    'ai': 40,
    'AI': 40,
    'machine-learning': 40,
    'machine learning': 40,

    'java': 41,

    'networking': 42,

    'golang': 43,
    'go': 43,

    'data-compression': 44,
    'data compression': 44,

    'webdev': 45,
    'web-dev': 45,

    'concurrency': 46,
    'parallelism': 46,
    'thread-pool': 46,
    'thread pool': 46,
    'async': 46,
    'multithreading': 46,
    'multi-threading': 46,
    'multi threading': 46,
    'atomics': 46,

    'memory-allocator': 47,
    'memory allocator': 47,
    'memory-allocation': 47,
    'memory allocation': 47,
    'memory-management': 47,
    'memory management': 47,

    'crypto': 48,
    'cryptography': 48,

    'maths': 49,
    'math': 49,
    'mathematics': 49,

    'software-rendering': 50,
    'software rendering': 50,
    'software-rasterization': 50,
    'software rasterization': 50,

    'assembly': 51,

    'vector-graphics': 52,
    'vector graphics': 52,

    'distributed-systems': 53,
    'distributed systems': 53,

    'formal-verification': 54,
    'formal verification': 54,

    'story': 55,
    'wildlife': 56,

    'forth': 57,

    'audio': 58,
    'audio-programming': 58,
    'audio programming': 58,

    'reverse-engineering': 59,
    'reversing': 59,

    'databases': 60,
    'database': 60,

    'legal-stuff': 61,
    'legal stuff': 61,
    'legal': 61,

    'simd': 62,
    'SIMD': 62,

    'travel': 63,
    'travelling': 63,
    'Travel': 63,

    'discussion': 64,
    'debate': 64,

    'osdev': 65,
    'os-dev': 65,
    'OS-Dev': 65,

    'text-rendering': 66,
    'text rendering': 66,

    'vulkan': 67,

    'learn-the-language-x': 68,
    'learn the language x': 68,

    'medicine': 69,
    'economy': 70,

    'crdt': 71,
    'CRDT': 71,

    'prolog': 72,

    'performance': 73,
    'optimization': 73,

    'music-theory': 74,
    'music theory': 74,

    'database-theory': 75,
    'database theory': 75,
    'database-internals': 75,
    'database internals': 75,

    'ships': 76,
    'cmake': 77,

    'text-editors': 78,
    'text editors': 78,
    'text-editor': 78,
    'text editor': 78,

    'system-theory': 79,
    'system theory': 79,
    'systems-theory': 79,
    'systems theory': 79,

    'history': 80,

    'fpga': 81,
    'FPGA': 81,

    'rng': 82,
    'RNG': 82,

    'linker': 83,
    'linkers': 83,

    'biology': 84,

    'path-finding': 85,
    'path finding': 85,

    'chemistry': 86,

    'encoding': 87,
    'encodings': 87,

    'iot': 88,
    'IoT': 88,
    'IOT': 88,

    'embedded': 89,

    'how-does-it-work': 90,
    'how does it work': 90,
    'how-it-works': 90,
    'how it works': 90,

    'file-system': 91,
    'file system': 91,

    'philosophy': 92,

    'search-engine': 93,
    'search engine': 93,
    'search-engine-theory': 93,
    'search engine theory': 93,

    'image-processing': 94,
    'image processing': 94,

    'hall-of-fame': 95,
    'hall of fame': 95,
    'hof': 95,
    'HOF': 95,

    'paradox': 96,
    'law': 96,

    'dsp': 97,
    'DSP': 97,

    'probabilistic-programming': 98,
    'probabilistic programming': 98,

    'browser-internal': 99,
    'browser internal': 99,
    'browser-internals': 99,
    'browser internals': 99,
    'browser-engine': 99,
    'browser engine': 99,

    'genetic-algorithm': 100,
    'genetic algorithm': 100,
    'genetic-algorithms': 100,
    'genetic algorithms': 100,

    'bit-manip': 101,
    'bit manip': 101,
    'bit-manipulation': 101,
    'bit manipulation': 101,

    'probabilistic-programming': 102,
    'probabilistic programming': 102,

    'accessibility': 103,

    'debugger-internals': 104,
    'debugger internals': 104,
    'debugger': 104,

    'wiki': 105,

    'terminal-emulator': 106,
    'terminal emulator': 106,
    'terminal-emulation': 106,
    'terminal emulation': 106,

    'chess-engine': 107,
    'chess engine': 107,

    'logic': 108,

    'QR': 109,
    'qr': 109,

    'statistics': 110,
    'stats': 110,
    'prob-stats': 110,
    'probabilities': 110,

    'critical-thinking': 111,
    'critical thinking': 111,

    'protocol': 112,
    'webgpu': 113,
    'blockchain': 114,

    'graph-theory': 115,
    'graph theory': 115,

    'typography': 116,

    'category-theory': 117,
    'category theory': 117,

    'terrain-generation': 118,
    'terrain generation': 118,
    'terrain-generator': 118,
    'terrain generator': 118,

    'quantum-computing': 119,
    'quantum computing': 119,

    'emu-dev': 120,
    'emulator-dev': 120,
    'emulator dev': 120,

    'lisp': 121,

    'complexity-theory': 122,
    'complexity theory': 122,

    'GPS': 123,
    'gps': 123,

    'CI/CD': 124,
    'ci-cd': 124,
    'ci': 124,

    'HoTT': 125,
    'hott': 125,
    'homotopy-type-theory': 125,

    'OCaml': 126,
    'Ocaml': 126,
    'ocaml': 126,

    'email': 127,
    'e-mail': 127,

    'backup': 128,

    'lambda-calculus': 129,
    'lambda calculus': 129,

    'engineering': 130,
    'Engineering': 130,

    'cooking': 131,
    'Cooking': 131,

    'markov-chain': 132,
    'Markov-Chain': 132,

    'functional-programming': 133,
    'Functional-Programming': 133,
    'FP': 133,

    'visualization': 134,
    'vizualization': 134,
    'visualisation': 134,
    'Visualization': 134,
    'Vizualization': 134,
    'Visualisation': 134,

    'computer-vision': 135,
    'computer vision': 135,
    'Computer-Vision': 135,
    'Computer Vision': 135,

    'Erlang': 136,
    'erlang': 136,

    'resume': 137,
    'Resume': 137,
    'CV': 137,

    'LaTeX': 138,
    'latex': 138,
}

if len(sys.argv) != 2:
    print('I need an argument: from what index should I start counting?')

index: int = int(sys.argv[1])

LINK: int = 0
TITLE: int = 1
DESCRIPTION: int = 2
TAGS: int = 3

links_list: List[str] = []
titles_list: List[str] = []

with open('./links.csv') as links:
    link_reader = csv.reader(links)
    for row in link_reader:
        links_list.append(row[1])
        titles_list.append(row[2])

with open('./index.txt', 'r') as f:
    links: List[Tuple[int, str, str, str]] = []
    links_tags: List[Tuple[int, int]] = []
    line_index = 1

    for line in f:
        attributes: List[str] = []
        current_str: str = ''
        inside_string: bool = False

        for ch in line:
            if ch == '"':
                current_str += ch
                inside_string = not inside_string

                if not inside_string:
                    attributes.append(current_str)
                    current_str = ''

            elif inside_string:
                current_str += ch

        links.append((index, attributes[LINK], attributes[TITLE], attributes[DESCRIPTION]))

        if attributes[LINK][1:-1] in links_list or attributes[TITLE][1:-1] in titles_list:
            #print(f'--------ERROR[line={line_index}]--------')
            #print(f'{attributes[TITLE]}({attributes[LINK]}) already exists!')
            pass

        def unquote_tag(tag: str) -> str:
            unquoted = tag[1:]
            return unquoted[:-1]

        tags = [t[1:][:-1] for t in attributes[TAGS:]]
        tags = ",".join(tags)
        #print(f'{attributes[LINK]},{attributes[TITLE]},{attributes[DESCRIPTION]},"{tags}"')
        
        for k in tag_mapping:
            print(f'"{k}","{tag_mapping[k]}"')

        for tag in attributes[TAGS:]:
            unquoted_tag = tag[1:]
            unquoted_tag = unquoted_tag[:-1]

            if unquoted_tag not in tag_mapping:
                #print(f'--------ERROR[line={line_index}]--------')
                #print(f'Tag "{unquoted_tag}" not found!!!!!\n')
                pass
            else:
                tag_id = tag_mapping[unquoted_tag]
                links_tags.append((index, tag_id))

        index += 1
        line_index += 1

    #print('--------links.csv--------')
    for element in links:
        #print(f'{element[0]},{element[1]},{element[2]},{element[3]}')
        pass

    #print('--------links_tags.csv--------')
    for element in links_tags:
        #print(f'{element[0]},{element[1]}')
        pass
