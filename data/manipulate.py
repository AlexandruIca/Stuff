#!/usr/bin/env python

import sqlite3
from argparse import ArgumentParser


parser: ArgumentParser = ArgumentParser(description='Query links')
parser.add_argument(
    '--db', type=str, help='Where is the sqlite database?', default='./information.db')
parser.add_argument('--tags', type=str,
                    help='Comma-separated list of tags')
parser.add_argument('--search', type=str, help='Fuzzy searching')

args = parser.parse_args()

connection = sqlite3.connect(args.db)


def with_cursor(fn):
    cursor = connection.cursor()
    fn(cursor)
    connection.commit()


if args.tags:
    print('Requested tags: ', args.tags.split(','))
    requested_tags = args.tags.split(',')

    def search_with_tags(cursor):
        for tag in requested_tags:
            tag_id = cursor.execute(
                'SELECT id FROM tags WHERE name = ?', (tag,))
        query = '''
           SELECT
             link_id
           FROM
             links_tags
           GROUP BY
             link_id
           HAVING
             max(tag_id = :tag_id1) = 1
             AND max(tag_id = :tag_id2) = 1
             AND ...;
        '''
elif args.search:
    def fuzzy_search(cursor):
        cursor.execute(
            'CREATE VIRTUAL TABLE IF NOT EXISTS search USING FTS5(title, description)')

        for row in cursor.execute('SELECT title, description FROM links').fetchall():
            cursor.execute(
                'INSERT INTO search(title, description) VALUES(?, ?)', (row[0], row[1]))

        for row in cursor.execute("SELECT * FROM search WHERE search MATCH ?", (str(args.search),)).fetchall():
            print(row)

    with_cursor(fuzzy_search)

connection.close()
