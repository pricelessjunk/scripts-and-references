#!/bin/bash
set -v

name=$1

rm files_"$name"/input.txt

ls -1 files_"$name"/| while read l; do echo file \'$l\' >> files_"$name"/input.txt; done

ffmpeg -f concat -i files_"$name"/input.txt -c copy "$name".ts
