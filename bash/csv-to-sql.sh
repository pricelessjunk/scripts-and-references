#!/bin/bash

# Converts csv files with heading to sql
# Outputs to a file out.sql
# 
# Usage: ./csv-to-sql.sh csv-file.csv

#Terminate early
set -e

# Accepts path to csv file
input=$1

if [[ -f out.sql ]]; then
	rm out.sql
fi;

# ctrl + v + m for ^M
sed 1d $input| sed 's/
//' |while IFS=, read -r id dob hvs rest; do
	while IFS=. read dd mm yy; do ddmm=$dd$mm; done <<< $dob;
	#echo $dob
	#echo $ddmm
	echo $hvs
	echo "update users set dob='$ddmm', hv_status=$hvs where id='$id';" >> out.sql 
done 
