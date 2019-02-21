#!-*- coding: utf8 -*-

#--------------------------------------------------
#TG CoDis
#obter-quantidade-palavras.py
#processes todos-juntos.txt - which contains all txts from a dataset (joined) - to count the terms in bag of words
#--------------------------------------------------


#---Imports
import sys


#---Variables
base = sys.argv[1]

item = []
classe = []
features = []
word = []
frequency = []

#---Read files with all 10 txts
### UPDATE PATH
with open("/codis/files/" + base + "/todos-juntos.txt" , "r") as f:
	base = f.readlines()


#creating item, class and features lists
for i in range(0, len(base)):
	item.append([x.strip() for x in base[i].split(" ")])
	classe.append(item[i][0])
	features.append([])
	for j in range(0, len(item[i])):
		features[i].append([x.strip() for x in item[i][j].split(":")])
		

#creating word and frequency lists
for i in range(0, len(features)):
	word.append([])
	frequency.append([])
	for j in range(1, len(features[i])-1):	#ignores first element - the class - and the last - #
		word[i].append(int(features[i][j][0]))
		frequency[i].append(float(features[i][j][1]))
 

W=0 


#adjusting W
for i in range (0, len(word)):
	if(W < max(word[i])):
		W = max(word[i]) 



print(W+1)
