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
source setList.txt
source setName.txt
mark=0

echo 'setName, setSpec, # of records, # of titles, # of creators, avg creators per record, # of dates, # of coverages, # of formats, # of types, # of 
subjects, avg 
subjects per record' 
>>fsudlReport$iso.csv

# Setting up the report loop
for i in ${setList[@]}; do
	echo "Analysing $i"
	setName=${setName[$mark]}
	recNum=`count ./harvest/$i* record$`
	if [ $recNum -eq 0 ]; then
		echo "$setName, $i, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0" >>fsudlReport$iso.csv
	else
		titleNum=`breaker title ./harvest/$i*`
		creatorNum=`breaker creator ./harvest/$i*`
		dateNum=`breaker date ./harvest/$i*`
		coverNum=`breaker coverage ./harvest/i*`
		formatNum=`breaker format ./harvest/i*`
		typeNum=`breaker type ./harvest/i*`
		subNum=`breaker subject ./harvest/$i*`
		echo $setName "," $i "," $recNum "," $titleNum "," $creatorNum "," $(( $creatorNum / $recNum )) "," $dateNum "," $coverNum "," $formatNum 
"," $typeNum "," $subNum "," $(( 
$subNum / $recNum )) >>fsudlReport$iso.csv
	fi
	mark=$(( $mark + 1 ))
done
printf "\nReport filed.\n\n"
