# codis
This repository contains the source code for CoDiS implementation in Python. Reference article: https://ieeexplore.ieee.org/document/8489287

---------------------
Reference Article:

L. V. N. Lapenda, R. H. W. Pinheiro and G. D. C. Cavalcanti, "An empirical analysis of Combined Dissimilarity Spaces," 2018 International Joint Conference on Neural Networks (IJCNN), Rio de Janeiro, 2018, pp. 1-8.
doi: 10.1109/IJCNN.2018.8489287

https://ieeexplore.ieee.org/document/8489287
---------------------


#1. Materials

## Datasets

In the folder 'files', you will find a sample dataset called 'tr23'. The dataset has 10 txts called 'teste1,teste2,...,teste10.txt'. Each of these corresponds to a fold generated through cross-validation.

### Dataset example:


	A file -> set of documents
	A line -> a document


Lines are as follows:

	
	3 31:6.000000 36:2.000000 37:1.000000 221:1.000000 233:1.000000 266:1.000000 270:2.000000 287:1.000000 


in which, 

- the first number represents the document (3, in this case)
- the sudsequent numbers are the attributes, where the number before the ":" is the term in bag of words, and the number after ":" is the number of times the term appears in the document. For instance, 31:6.000000 means that term 31 appears 6 times in this document. Term 31 is the one that comes in thirty first position in bag of words.  




#2. Step by Step:


	For each cross-validation round:
		Training:
		1. [if 'TFIDF' set] Convert data from TF to TF-IDF (term-frequency inverse-document-frequency).
		2. Perform Bootstraping in order to obtain L sets of same size of X (documents in each Xl are picked randomly. It is important to keep the size of the original set X for every Xl - with replacement).
		3. Generate representation sets, each of them with Q documents, where Q = 20% of X size. The documents is each representation set are picked randomly.
		4. Generate matrices D(Xl, Rl) with metrics: euclidian or cosine distance
		5. Train L classifiers (SVM or Decision Trees)
		Testing:
			For each document on test set Y:
			7. Pick the same Representation sets used during training for each l
			8. Generate matrices D(yj, Rl) with metrics: euclidian or cosine distance
			9. Run classifiers generated in training phase
			10. Pick the winning class based on majority vote


#3. Scripts execution order and explanation


Please, be aware that you should revisit every python file so you can update with paths to your system, keep the structure of folders under /codis as it is. You can search for ### in code to know where you should add your path.

Additionally in treinamento.py the code is set to run with threads, if you don't want it just comment the part between the sentence 'WITH PARALLEL PROCESSING' and 'WITHOUT PARALLEL PROCESSING' and uncomment the rest.

## 1 step - criar_pastas_scores.sh

This is a script to create the folders for each combination of parameter under a specified dataset name. E.g. /SVM-tf-cosseno, which stands for a folder where results for SVM, TF and Cosine Distance are stored.


## 2 step - juntar-txt_call.py 

This script has two main functions:

1. Join every txt file in a single file:

With a single joined file it is possible to count the total number os terms in bag of words - corpus. The generated file is called 'todos-juntos.txt'

2. Join every txt file belonging to a specific fold into a single file:

Every txt that belongs to the same fold should be joined. Ten files named 'fold x-junto.txt', where x is the fold number, are generated in this step.


## 3 step - obter_quantidade_palavras_call.py

This script uses 'todos-juntos.txt', from 1 step, in order to execute the instructions to obtain the total number of terms in bag of words for each dataset - corpus. This information is useful to set a variable in training phase.


## 4 step - run.sh

This script will basically run every other script you need. You just have to set these parameters:


export Base=tr23
export L=70
export W=5833
export Classifier=SVM
export Input=tf
export Metric=euclidiana

where,

Base = dataset name
L = L to be used
W = number of words returned in previous step
Classifier = whether you want to use 'SVM' or 'AD' (Decision Tree)
Input = input format. Can be 'TF' or 'TFIDF'
Metric = distance measure to compute dissimilarity matrices. Options are: 'euclidiana' or 'cosseno'

Attention! You should update teste_call.sh with the number of terms for each fold as, in a dataset, some folds might have a few more terms than others.

## Visualize performance measures

The files are stored under the folder [YOUR DATASET]/[YOUR CONFIGURATION OF PARAMETERS].  
e.g. 'tr23/SVM-tf-cosseno', which means it was run on dataset 'tr23' with parameters 'SVM', 'TF' and 'Cosine Distance'.

