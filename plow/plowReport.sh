#!/bin/bash

# Define report functions
breaker () {
	python /home/mmiguez/bin/dc_breaker/dc_breaker.py -e $1 $2 | wc -l
}
# Define counting function
count () {
	xmlstarlet el $1 | grep $2 | wc -l
}

# Read date and start report
iso=`date -I`
touch /home/mmiguez/bin/plow/fsudlReport$iso.csv

# Read set list into array
source /home/mmiguez/bin/plow/assets/setSpec.txt
source /home/mmiguez/bin/plow/assets/setName.txt
mark=0

echo 'setSpec, # of records, # of titles, # of creators, avg creators per record, # of dates, # of coverages, # of formats, # of types, # of subjects, avg subjects per record' >> /home/mmiguez/bin/plow/fsudlReport$iso.csv

# Setting up the report loop
for i in ${setList[@]}; do
	echo "Analysing $i"
	setName=${setName[$mark]}
	recNum=`count /home/mmiguez/bin/plow/harvest/$i* record$`
	if [ $recNum -eq 0 ]; then
		printf '%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0\n' $i >> /home/mmiguez/fsudlReport$iso.csv
	else
		titleNum=`breaker title /home/mmiguez/bin/plow/harvest/$i*`
		creatorNum=`breaker creator /home/mmiguez/bin/plow/harvest/$i*`
		dateNum=`breaker date /home/mmiguez/bin/plow/harvest/$i*`
		coverNum=`breaker coverage /home/mmiguez/bin/plow/harvest/$i*`
		formatNum=`breaker format /home/mmiguez/bin/plow/harvest/$i*`
		typeNum=`breaker type /home/mmiguez/bin/plow/harvest/$i*`
		subNum=`breaker subject /home/mmiguez/bin/plow/harvest/$i*`
		printf '%s, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f, %.2f\n' $i $recNum $titleNum $creatorNum $(( $creatorNum / $recNum )) $dateNum $coverNum $formatNum $typeNum $subNum $(( $subNum / $recNum )) >> /home/mmiguez/fsudlReport$iso.csv
	fi
	mark=$(( $mark + 1 ))
done
printf "\nReport filed.\n\n"