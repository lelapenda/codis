#!/bin/bash
clear



for i in {1..10}
do
	Fold=$i
	printf "\n\n$i\n"
	python ../PyScripts/metricas_desempenho.py $Base $Fold $Classifier $Input $Metric
done