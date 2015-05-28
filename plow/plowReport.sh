#!/bin/bash

# Define report functions
breaker () {
	python ~/bin/dc_breaker/dc_breaker.py -e $1 $2 | wc -l
}
# Define counting function
count () {
	xmlstarlet el $1 | grep $2 | wc -l
}

# Read date and start report
iso=`date -I`
touch fsudlReport$iso.csv

# Read set list into array
source assets/setSpec.txt
source assets/setName.txt
mark=0

echo 'setSpec, # of records, # of titles, # of creators, avg creators per record, # of dates, # of coverages, # of formats, # of types, # of subjects, avg subjects per record' >> fsudlReport$iso.csv

# Setting up the report loop
for i in ${setList[@]}; do
	echo "Analysing $i"
	setName=${setName[$mark]}
	recNum=`count ./harvest/$i* record$`
	if [ $recNum -eq 0 ]; then
		printf '%s, 0, 0, 0, 0, 0, 0\n' $i >> fsudlReport$iso.csv
	else
		titleNum=`breaker title ./harvest/$i*`
		creatorNum=`breaker creator ./harvest/$i*`
		subNum=`breaker subject ./harvest/$i*`
		printf '%s, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n' $i $recNum $titleNum $creatorNum $(( $creatorNum / $recNum )) $subNum $(( $subNum / $recNum )) >> fsudlReport$iso.csv
	fi
	mark=$(( $mark + 1 ))
done
printf "\nReport filed.\n\n"
