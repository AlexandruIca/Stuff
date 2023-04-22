#!/usr/bin/env python3

import csv
import sys


def load_rows_from_file(path):
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        next(reader)

        for row in reader:
            yield row


def get_link_for_row(row):
    return f'{{ id: {row[0]}, url: "{row[1]}", title: "{row[2]}", description: "{row[3]}" }}'


def get_tag_from_row(row):
    return f'{{ id: {row[0]}, name: "{row[1]}" }}'


def get_associative_table_from_row(row):
    return f'{{ link_id: {row[0]}, tag_id: {row[1]} }}'


def read(path, callback):
    result = ''
    row_num = 0

    for row in load_rows_from_file(path):
        try:
            result += (callback(row) + ',\n            ')
            row_num += 1
        except IndexError:
            print(f'IndexError at line {row_num}')
        except:
            print(f'Uncaught exception at line {row_num}')

    return result


if __name__ == '__main__':
    config = {
        'links_tags': get_associative_table_from_row,
        'links': get_link_for_row,
        'tags': get_tag_from_row,
    }

    final_output = ''

    with open('./template.html', 'r') as template:
        final_output = template.read()

    for key in config:
        content = read(f'./{key}.csv', config[key])
        final_output = final_output.replace(f'${key}', content)

    with open('./index.html', 'w') as output:
        output.write(final_output)
