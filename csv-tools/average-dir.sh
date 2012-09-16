#!/bin/bash
for dir in $1*;
do
	echo "Calling csv-average.py on " $dir	
	./csv-average.py -rw $dir ./`basename $dir`.csv


done
