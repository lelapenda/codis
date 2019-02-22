#!-*- coding: utf8 -*-

#--------------------------------------------------
#TG CoDis
#teste.py
#test for each fold
#--------------------------------------------------


#---Imports
import numpy as np
import pickle
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.spatial import distance
from scipy.stats import mode
from math import log
from math import sqrt
import multiprocessing
from multiprocessing import Process, Queue
import sys



#---Variables-----------------------
base = sys.argv[1]
L = sys.argv[2]
W = sys.argv[3]
Q = sys.argv[4]
foldTeste = sys.argv[5]
classifier = sys.argv[6]
inputFormat = sys.argv[7]
metric = sys.argv[8]

L = int(L) #number of classifiers
W = int(W)	#VARIABLE FOR EACH DATASET - number of words in bag of words for each dataset (set of documents - corpus) - for all txts
foldTeste = int(foldTeste)	#VARIABLE FOR EACH FOLD - currently fold being processed
Q = int(Q)	#VARIABLE FOR EACH FOLD - obtained in treinamento.py: represents 20% of the number of documents 


'''
#in case you want to set the variables here instead of in the sh scripts - useful for testing

base="wap"
L = 70
W = 8461
fold = 1 
classifier="SVM"
inputFormat="tf"
metric="euclidiana"
'''

item = []
classe = []
features = []
word = []
frequency = []
mR=[]
mRid = []
model = []
mYid=[]
Ntraining = 0 #VARIABLE FOR EACH DATASET (NUMBER OF DOCUMENTS IN TRAINING PHASE) - TO BE SET
mG = []
mYDistribution = []
mJ = []
m = []
y = []
processes = []
results = [] #for classifiers' results
documentVotes = []
finalClass= []
acuracia = 0


#---Reading previously saved data-----------------------

#reading Rls
for l in range (0,L):
	### UPDATE PATH
	mR.append(np.load("/codis/files/" + base + "/fold " + str(foldTeste) + "/Rls/Rl " + str(l+1) + ".npy"))

#reading Rls id
for l in range (0,L):
	### UPDATE PATH
	mRid.append(np.load("/codis/files/" + base + "/fold " + str(foldTeste) + "/Rls_ID/Rl " + str(l+1) + ".npy"))

#reading all Xs matrix
### UPDATE PATH
mXs = np.load("/codis/files/" + base + "/fold " + str(foldTeste) + "/All_Xs/mXs.npy")
Ntraining = len(mXs) 
mXs = np.delete(mXs, W, 1) #deleta coluna W


#reading classifiers' models
for l in range(0,L):
	### UPDATE PATH
	file = open("/codis/files/" + base + "/fold " + str(foldTeste) + "/" + classifier + "/modelos/modelo " + str(l+1), "rb")
	model.append(pickle.load(file))



#---Reading test fold-----------------------

### UPDATE PATH
with open("/codis/files/" + base + "/teste" + str(foldTeste) + ".txt") as f:
    content = f.readlines() #content of type list


#---Processing input - matrix format-----------------------


#creating item, class and features list
for i in range(0, len(content)):
	item.append([x.strip() for x in content[i].split(" ")])
	classe.append(item[i][0])
	features.append([])
	for j in range(0, len(item[i])):
		features[i].append([x.strip() for x in item[i][j].split(":")])
		

#creating terms and frequency lists 
for i in range(0, len(features)):
	word.append([])
	frequency.append([])
	for j in range(1, len(features[i])-1):	#ignores first element - the class - and the last - #
		word[i].append(int(features[i][j][0]))
		frequency[i].append(float(features[i][j][1]))
 

N = len(content) 


#--Writing into sparse matrix

#creating matrix
mtf = csr_matrix((N, W+1), dtype=np.float64).toarray() #n in the number of lines and W number of columns.

#populate matrix
for i in range (0, N):
	for j in range(0, len(word[i])):
		mtf[i][word[i][j]] = frequency[i][j]

mtf = np.delete(mtf, 0, 1)


#---TF-IDF------------------------------------


if inputFormat=="tfidf":
	print "tfidf"
	transformer = TfidfTransformer(smooth_idf=True)
	mtfidf = transformer.fit_transform(mtf)
	mtfidf = mtfidf.toarray()
	mtf=mtfidf
elif inputFormat=="tf": 
	print "tf"
	mtf=mtf
else:
	print "Exiting"
	exit()


#--Creating mY matrix
mY = mtf




#---Representation Transformation-----------------------




#--Euclidian and Cosine ----------------

#--mG is a atrix: X vs X - General Matrix 

if metric=="euclidiana":
	print "euclidiana"
	for i in range(0, N):
		mG.append([])
		for k in range(0, Ntraining):
			mG[i].append(distance.euclidean(mY[i],mXs[k]))
elif metric=="cosseno":
	print "cosseno"
	for i in range(0, N):
		mG.append([])
		for k in range(0, Ntraining):
			mG[i].append(distance.cosine(mY[i],mXs[k]))
else:
	print "Exiting"
	exit()



#Creating mj matrix
for l in range(0, L):
	mJ.append([])
	for i in range(0, N):
		mJ[l].append([])
		for j in range(0, Q):
			mJ[l][i].append(mG[i][mRid[l][j]])


del mG

#---Applying classifiers individually-----------------------


for l in range(0,L):
	results.append(model[l].predict(mJ[l])) #results vector has L position, each of which has the classification results of N documents in test data


#--- Majority Vote----------------------------------------------


for i in range (0,N):
	documentVotes.append([])
	for l in range (0, L):
		documentVotes[i].append(results[l][i]) #documentVotes' goal is to 'invert' results, this way documentVotes will be the same size as N, number of documents in test data, and each element has L positions indicating the class of document i for each L classifier.


#Storing only most frequent label
for i in range (0,N):
	finalClass.append(mode(documentVotes[i])[0][0])




#---Saving real class and predicted class into file -----------------------

#to be consumed later when computing performance measures

#writing real class
### UPDATE PATH
file = open("/codis/files/" + base + "/fold " + str(foldTeste) + "/" + classifier + "/classe_real", "w")
for item in classe:
	file.write("%s " % item)

file.close()


#writing predicted class
### UPDATE PATH
file = open("/codis/files/" + base + "/fold " + str(foldTeste) + "/" + classifier + "/classe_predita", "w")
for item in finalClass:
	file.write("%s " % item)

file.close()

