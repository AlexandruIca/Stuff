#!/usr/bin/env bash

pandoc --metadata pagetitle="Useful Links" -s index.md -o index.html --css=./index.css
