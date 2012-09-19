#!/bin/bash
#for dir in $1*;
#./average-dir.sh ~/Study/TestData/1/ 10 > 1.csv

#do
	#echo "Calling csv-average.py on " $1	

	for i in {0..99}
	do
		#echo "Files:"	   
		{ echo -n $i", " && find $1 | grep "\."$i"\.json" |  head -n $2 | xargs ./json-dump.py "population>.Critter[Fitness.Changes,Fitness.TotalJourneyMinutes,Rank]" | ./csv-collate.py -n 1 -a 6 -m 6,9 -M 6 -y 100,11,6,9; }
#	done
	
	


done
