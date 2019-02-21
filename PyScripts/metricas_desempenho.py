#!-*- coding: utf8 -*-

#--------------------------------------------------
#TG CoDis
#metricas_desempenho.py
#Computes performance measures
#--------------------------------------------------

#---Imports
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
import sys


#---Variables
base = sys.argv[1]
foldTeste = sys.argv[2]
classifier = sys.argv[3]
inputFormat = sys.argv[4]
metric = sys.argv[5]


foldTeste = int(foldTeste)	#VARIABLE FOR EACH FOLD - currently fold being processed

classe_real = []
classe_predita = []


#---Reading class files

#class_real
### UPDATE PATH
file = "/codis/files/" + base + "/fold " + str(foldTeste) + "/" + classifier + "/classe_real"
with open(file, 'r') as f:
    content = f.read()

classe_real = content.split(" ")
classe_real.pop() #removing classe_real last position, with garbage values


#predicted_class
### UPDATE PATH
file = "/codis/files/" + base + "/fold " + str(foldTeste) + "/" + classifier + "/classe_predita"
with open(file, 'r') as f:
    content = f.read()

classe_predita = content.split(" ")
classe_predita.pop()



#---Metrics

#F1 score
f1_macro = f1_score(classe_real, classe_predita, average='macro')  
f1_micro = f1_score(classe_real, classe_predita, average='micro')

print "\nF1-Macro: %s" % f1_macro
print "\nF1-Micro: %s" % f1_micro


#writing metrics
### UPDATE PATH
file = open("/codis/files/" + base + "/" + classifier + "-" + inputFormat + "-" + metric + "/Score_fold" + str(foldTeste), "w")
file.write("\nF1-Macro: %s" % f1_macro)
file.write("\nF1-Micro: %s" % f1_micro)
file.close()
