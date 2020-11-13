#!/bin/bash
for f in $( grep -e [0-9] sysNum.csv ); do
	printf "%s" "sys=$f or " >> sysNum.txt
done
echo "sysNum.txt created"
