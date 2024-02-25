#!/bin/bash

pyinstaller StreamCat.py
mkdir "dist/StreamCat/_internal/stream_cat/"
cp -r stream_cat/assets/ dist/StreamCat/_internal/stream_cat/
cp StreamCat.png dist/StreamCat/
cp StreamCat.svg dist/StreamCat/
cp create-desktop-entry.sh dist/StreamCat/