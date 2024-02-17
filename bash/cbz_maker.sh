#!/bin/bash

for dir in *; do
	if [[ -d $dir ]]; then
		zip -0 "$dir".cbz "$dir"/*.jpg;
	fi	
done
