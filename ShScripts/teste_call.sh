#!/bin/bash
clear



for i in {1..10}
do
	Fold=$i
	printf "\n$i\n\n"

	if [ "$Fold" -eq "6" ];
	then
		Q=73		#update the number of terms accordingly
	elif [ "$Fold" -eq "7" ];
	then
		Q=74
	elif [ "$Fold" -eq "8" ];
	then
		Q=74
	elif [ "$Fold" -eq "9" ];
	then
		Q=74
	elif [ "$Fold" -eq "10" ];
	then
		Q=74
	else
		Q=72
	fi

	python ../PyScripts/teste.py $Base $L $W $Q $Fold $Classifier $Input $Metric

done
