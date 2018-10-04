#!/bin/bash

DC=(contributor coverage creator date description format identifier language publisher relation rights source subject title type)

mkdir analysis
mkdir analysis/top

for file in $( ls *.xml ); do
    echo $file
    printf '\n# %s\n' "$file" > analysis/top/${file/.xml/}.md
#    echo >> analysis/top/${file/.xml/}.md
    for elem in ${DC[*]}; do
        echo ${file/.xml/}_$elem
        printf "\n## %s\n" "$elem" >> analysis/top/${file/.xml/}*
#        echo ""  >> analysis/top/${file/.xml/}*
        xmlstarlet sel -N dc=http://purl.org/dc/elements/1.1/ -t -v //dc:$elem $file  > analysis/${file/.xml/}_$elem.md
        while read -r line
            do
                #echo "$line"
                printf "* %s\n" "$line" >> analysis/top/${file/.xml/}*         
            done < <( cat analysis/${file/.xml/}_$elem.md | sort | uniq -c | sort -n -r | head )
    done
done

cat analysis/top/*.md > master.md
pandoc --latex-engine=xelatex master.md -o $1.pdf

