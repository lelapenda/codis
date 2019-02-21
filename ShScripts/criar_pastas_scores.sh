#!/bin/bash
clear


str='fold'
Base=tr23 #update with your dataset name


cd ../files
cd $Base


mkdir SVM-tf-euclidiana
mkdir SVM-tf-cosseno
mkdir SVM-tfidf-euclidiana
mkdir SVM-tfidf-cosseno
mkdir AD-tf-euclidiana
mkdir AD-tf-cosseno
mkdir AD-tfidf-euclidiana
mkdir AD-tfidf-cosseno