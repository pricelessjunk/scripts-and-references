#!/bin/bash

name=$1
link=$2

# Fix the before after variables here first. And the response file
# TODO take from first link
python3 downloader.py "$name" "$link"

./links_"$name"

./ffmpeg.sh "$name"
