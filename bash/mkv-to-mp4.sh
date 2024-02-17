#!/bin/bash

# Converts mkv files to mp4 files. To use on any other file type like avi, 
# just change the variable FILE_TYPE
# Usage: ./mkv-to-mp4.sh

set -e  # Terminate early

FILE_TYPE="*.mkv"
for f in $FILE_TYPE; do
    if [[ -f "$f" ]]; then
        filename=$(echo "$f" | rev | cut -f 2- -d '.' | rev)
        newname=$(echo "$filename"".mp4")
        ffmpeg -i "$f" -c:v copy -c:a copy -y -strict -2 "$newname"
    fi
done
