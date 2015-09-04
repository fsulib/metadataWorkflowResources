#!/bin/bash

# Ready the outputs
rm -rf /home/mmiguez/bin/plow/harvest
mkdir /home/mmiguez/bin/plow/harvest
rm /home/mmiguez/bin/plow/assets/setSpec.xml
rm /home/mmiguez/bin/plow/assets/setSpec.txt
rm /home/mmiguez/bin/plow/assets/setName.txt

#build arrays
touch /home/mmiguez/bin/plow/assets/setSpec.xml
touch /home/mmiguez/bin/plow/assets/setSpec.txt
touch /home/mmiguez/bin/plow/assets/setName.txt
python /home/mmiguez/bin/plow/assets/setSpecFetch.py

printf 'setList=(' > /home/mmiguez/bin/plow/assets/setSpec.txt
for setSpec in $( xmlstarlet sel -T -t -v //setSpec /home/mmiguez/bin/plow/assets/setSpec.xml ); do
	printf '%s ' $setSpec >> /home/mmiguez/bin/plow/assets/setSpec.txt
done
printf ')' >> /home/mmiguez/bin/plow/assets/setSpec.txt

printf 'setName=(' > /home/mmiguez/bin/plow/assets/setName.txt
for setName in $( xmlstarlet sel -T -t -v //setName /home/mmiguez/bin/plow/assets/setSpec.xml ); do
	printf '%s ' $setName >> /home/mmiguez/bin/plow/assets/setName.txt
done
printf ')' >> /home/mmiguez/bin/plow/assets/setName.txt

# Define report functions
breaker () {
	python /home/mmiguez/bin/dc_breaker/dc_breaker.py -e $1 $2 | wc -l
}
count () {
	xmlstarlet el $1 | grep $2 | wc -l
}


# Reading set data into the array
source /home/mmiguez/bin/plow/assets/setSpec.txt
source /home/mmiguez/bin/plow/assets/setName.txt
iso=`date -I`
mark=0

# Setting up the loop
for i in ${setList[@]}; do
	# Set up the harvest
	python /home/mmiguez/bin/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -s $i -o /home/mmiguez/bin/plow/harvest/$i$iso.xml
done
python /home/mmiguez/bin/pyoaiharvester/pyoaiharvest.py -l http://fsu.digital.flvc.org/oai2 -m mods -o/home/mmiguez/bin/plow/harvest/modsRoot$iso.xml
printf "\n\nHarvest complete.\n\n"

# Start report
touch /home/mmiguez/fsudlReport$iso.csv
echo 'setSpec, # of records, # of titles, # of creators, avg creators per record, # of dates, # of coverages, # of formats, # of types, # of subjects, avg subjects per record' >> /home/mmiguez/fsudlReport$iso.csv

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

# archive harvest
tar cvf - /home/mmiguez/bin/plow/harvest/* | gzip > /home/mmiguez/fsudlharvest$iso.tar.gz
printf "\nResults archived.\n\n"
