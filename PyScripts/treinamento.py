#!-*- coding: utf8 -*-

#--------------------------------------------------
#TG CoDis
#treinamento.py
#processing txts for each training fold - reading and writing into sparse martix, transforming into TF-IDF, Bootstrapping, Representation Transformation, classifiers training and model persistence
#--------------------------------------------------

#---Imports----------------------------
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.utils import resample
from scipy.spatial import distance
import pickle
import multiprocessing
from multiprocessing import Process, Queue
from math import log
from math import sqrt
import sys


#---Variables------------
base = sys.argv[1]
L = sys.argv[2]
W = sys.argv[3]
fold = sys.argv[4]
classifier = sys.argv[5]
inputFormat = sys.argv[6]
metric = sys.argv[7]

L = int(L) #number of classifiers
W = int(W)	#VARIABLE FOR DATASET - number of terms in bag of words for each dataset(set of documents - corpus) - for all txts
fold = int(fold)	#VARIABLE FOR EACH FOLD - currently fold being processed

'''
#in case you want to set the variables here instead of in the sh scripts - useful for testing


base="syskill"
L = 20
W = 4340
fold = 1 
classifier="SVM"
inputFormat="tf"
metric="cosseno"
'''

item = []
classe = []
features = []
word = []
frequency = []
N = 0 #number of documents - per fold - to be set
mX = []
mXid = []
mRid = []
mR = []
Q = 0 #number of documents in each representation set - per fold - to be set
Ldiv = 0 #number of classifiers to be precossed in each cpu - to be set
mG = [] #general matrix X vs X
mGDistribution = []
mJ = []
mJclasse = []
processes = []
m=[]
y=[]
model = []
rs = [i for i in range(0,L*2)] #variable to be used in random_state. This variable has 200 numbers. When changing the number of random-state different subsets will be chosen. It has length L*2 due to the two resamples: Xs and Rs


#---Reading and preparing file------------------

#output example for this step:
#content: [ '3 31:6.000000 36:2.000000', '3 14:4.000000 28:2.000000' ]
#item: [ ['3', '31:6.000000', '36:2.000000'],['3', '14:4.000000', '28:2.000000'] ]
#classe: [ '3', '3' ]
#features: [ [['3'], ['31', '6.000000'], ['36', '2.000000']], [['3'], ['14', '4.000000'], ['28', '2.000000']] ]
#word: [ ['31', '36'], ['14', '28'] ]
#frequency: [ ['6.000000', '2.000000'], ['4.000000', '2.000000'] ]



#reading txt line by line (stored as list elements)

### UPDATE PATH
with open("/codis/files/" + base + "/fold" + str(fold) + "-junto.txt") as f:
    content = f.readlines() #content of type list


#creating item, class and features lists
for i in range(0, len(content)):
	item.append([x.strip() for x in content[i].split(" ")])
	classe.append(item[i][0])
	features.append([])
	for j in range(0, len(item[i])):
		features[i].append([x.strip() for x in item[i][j].split(":")])
		

#creating word and frequency list
for i in range(0, len(features)):
	word.append([])
	frequency.append([])
	for j in range(1, len(features[i])-1):	#ignores first element - the class - and the last - #
		word[i].append(int(features[i][j][0]))
		frequency[i].append(float(features[i][j][1]))
 

N = len(content) 
ids = [i for i in range(0,N)]


#---Writing into sparse matrix ------------------

#creating matrix 
mtf = csr_matrix((N, W+2), dtype=np.float64).toarray() #where n in the number of lines and W+2 the number of columns. W+2 because there is an ID column for the class, W words + the ID of column zero with no information

#populating matrix 
for i in range (0, N):
	for j in range(0, len(word[i])):
		mtf[i][word[i][j]] = frequency[i][j]


#deleting column zero as there is no word zero
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


#---Adding ID column to document
for i in range (0, N):
	mtf[i][W] = i	#adds a column with document ID so it is possible to recover the class later

#---Excluding document ID column
mtf_semID = np.delete(mtf, W, 1) #delets column W



#saving matrix with all Xs to be used in test phase

### UPDATE PATH
np.save("/codis/files/" + base + "/fold " + str(fold) + "/All_Xs/mXs", mtf)



#---Bootstrapping-----------------------------


for l in range(0,L):
	mXid.append(resample(ids, replace=True, n_samples=N, random_state=rs[l]))


#creating Rls
Q = int(0.2 * N)
print "Q"
print Q
	
for l in range(0,L):
	mR.append(resample(mtf, replace=True, n_samples=Q, random_state=rs[l+L]))


#creating matrix with document ID in every Rls - important to keep track for metrics computation
for l in range(0,L):
	mRid.append([])
	for i in range(0,Q):
		mRid[l].append(int(mR[l][i][W]))


#deleting document ID column
for l in range(0,L):
		mR[l] = np.delete(mR[l], W, 1) #delets W column


#writing Rls in file for test phase
for l in range (0,L):
		### UPDATE PATH
		np.save("/codis/files/" + base + "/fold " + str(fold) + "/Rls/Rl " + str(l+1), mR[l])

del mR


#writing Rls id in file for test phase
for l in range (0,L):
		### UPDATE PATH
		np.save("/codis/files/" + base + "/fold " + str(fold) + "/Rls_ID/Rl " + str(l+1), mRid[l])



#---Representation Transformation-----------------------


if metric=="euclidiana":
	print "euclidiana"
	for i in range(0, N):
		mG.append([])
		for k in range(0, N):
			mG[i].append(distance.euclidean(mtf_semID[i],mtf_semID[k]))
elif metric=="cosseno":
	print "cosseno"
	for i in range(0, N):
		mG.append([])
		for k in range(0, N):
			mG[i].append(distance.cosine(mtf_semID[i],mtf_semID[k]))
else:
	print "Exiting"
	exit()



for l in range(0, L):
	mJ.append([])
	mJclasse.append([])
	for i in range(0, N):
		mJ[l].append([])
		mJclasse[l].append(classe[mXid[l][i]])
		for j in range(0, Q):
			mJ[l][i].append(mG[mXid[l][i]][mRid[l][j]])


del mG


#---Train Classifiers----------------------------------


#WITH PARALLEL PROCESSING

#1. multiprocessing variables

workers = multiprocessing.cpu_count()
Ldiv = L/workers
m=[]
y=[] 
mc=[]
for i in range(0, workers):
	m.append([])
	mc.append([])
	y.append(Queue())



#2.Set matrix to distribute documents accross cpus
for cpu in range(0, workers):
	ini = cpu * Ldiv
	if cpu != workers-1:	#cpu isn't last, treatment is need in order to deal with cases like: N=46, Ndiv=11, 11*4 workers = 44, here 2 wouldn't be processed
		fim = ini + Ldiv
	else: 
		fim = L
	for l in range(ini , fim):
		m[cpu].append(mJ[l])
		mc[cpu].append(mJclasse[l])




def Classifica(mq, mqclasse, y, classifier):
	if classifier=="SVM":
		from sklearn.svm import LinearSVC
		print "SVM"
		for l in range(0,len(mq)):
			modelo = LinearSVC(C=1)
			modelo.fit(mq[l],mqclasse[l])
			y.put(modelo)
	elif classifier=="AD":
		from sklearn import tree
		print "AD"	
		for l in range(0,len(mq)):
			modelo = tree.DecisionTreeClassifier()
			modelo.fit(mq[l], mqclasse[l]) 
			y.put(modelo)
	else:
		print "Exiting"
		exit()
	print "finalizado"



#3. Calling processes
for w in range(0,workers):
	p = Process(target=Classifica, args=(m[w], mc[w], y[w], classifier))
	p.start()
	processes.append(p)



#4. Generate models with organized values
for cpu in range(0, workers):
	ini = cpu * Ldiv
	if cpu != workers-1:	
		fim = ini + Ldiv
	else: 
		fim = L
	for i in range(ini, fim):
		#model.append(y[cpu].get())
		#---Persist models
		### UPDATE PATH
		file = open("/codis/files/" + base + "/fold " + str(fold) + "/" + classifier + "/modelos/" + "modelo "+ str(i+1), "wb")
		s = pickle.dump(y[cpu].get(),file)
		file.close()


'''
#WITHOUT PARALLEL PROCESSING

#SVM, MLP

if classifier=="SVM":
	from sklearn.svm import LinearSVC
	print "SVM"
	for l in range(0,L):
		print l
		model.append(LinearSVC(C=1))
		model[l].fit(mJ[l],mJclasse[l])
elif classifier=="AD":
	from sklearn import tree
	print "AD"	
	for l in range(0,L):
		model.append(tree.DecisionTreeClassifier())
		model[l].fit(mJ[l], mJclasse[l]) 
else:
	print "Exiting"
	exit()

'''


#---Persisting models--------------------------------
for l in range(0,L):
	### UPDATE PATH
	file = open("/codis/files/" + base + "/fold " + str(fold) + "/" + classifier + "/modelos/" + "modelo "+ str(l+1), "wb")
	s = pickle.dump(model[l],file)
	file.close()


