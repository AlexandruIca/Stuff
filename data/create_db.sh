#!/usr/bin/env sh

# TODO: from '# CPP Tools And Libraries'

sqlite3 information.db << EOF
DROP TABLE IF EXISTS links;
DROP TABLE IF EXISTS tags;
DROP TABLE IF EXISTS links_tags;

CREATE TABLE links(
    id INTEGER PRIMARY KEY,
    url TEXT,
    title TEXT,
    description TEXT
);

CREATE TABLE tags(
    id INTEGER PRIMARY KEY,
    name TEXT
);

CREATE TABLE links_tags(
    link_id INTEGER,
    tag_id INTEGER,
    FOREIGN KEY (link_id) REFERENCES links (id),
    FOREIGN KEY (tag_id) REFERENCES tags (id),
    PRIMARY KEY (link_id, tag_id)
);

.mode csv

.import ./links.csv links --skip 1
.import ./tags.csv tags --skip 1
.import ./links_tags.csv links_tags --skip 1
EOF

# SELECT
#   l.title || ' - ' || l.description || ' {' || t.name || '}' AS info
# FROM
#   links_tags lt
# JOIN
#   links l ON (l.id = lt.link_id)
# JOIN
#   tags t ON (t.id = lt.tag_id)
# LIMIT 20;

# Get tags for a link id:
# SELECT
#   t.name
# FROM
#   links_tags lt
# JOIN
#   tags t ON (t.id = lt.tag_id)
# WHERE
#   lt.link_id = :known_link_id;

# Get links that have at least some tags attached to them:
# SELECT
#   link_id
# FROM
#   links_tags
# GROUP BY
#   link_id
# HAVING
#   max(tag_id = :tag_id1) = 1
#   AND max(tag_id = :tag_id2) = 1
#   AND ...;
