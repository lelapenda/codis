#!/bin/bash
clear


for i in {1..10}
do
	Fold=$i
	printf "\n$i\n\n"
	python ../PyScripts/treinamento.py $Base $L $W $Fold $Classifier $Input $Metric
done