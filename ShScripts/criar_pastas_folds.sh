#!/bin/bash
clear


str='fold'


cd ../files
cd $Base

for i in {1..10}
do
	Fold=$i
	mkdir $str\ $Fold
	cd $str\ $Fold
	mkdir All_Xs
	mkdir Xls
	mkdir Xls_ID
	mkdir Rls
	mkdir Rls_ID
	mkdir $Classifier
	cd $Classifier
	mkdir modelos
	cd ../..
done

