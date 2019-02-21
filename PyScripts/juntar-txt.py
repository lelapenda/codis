#!-*- coding: utf8 -*-

#--------------------------------------------------
#CoDis
#juntar-txt.py
#processing raw txts: 1. joining all txts, 2. joining every txt in same folder i
#--------------------------------------------------

#---Imports
import sys


#---Variables
base = sys.argv[1]
arquivo = ["posicaoNULA","teste1.txt", "teste2.txt","teste3.txt","teste4.txt","teste5.txt","teste6.txt","teste7.txt","teste8.txt","teste9.txt","teste10.txt"]


#---Joining all folds in single file
for i in range (1,11):
	### UPDATE PATH
	with open("/codis/files/" + base + "/todos-juntos.txt", "a") as f: 
			### UPDATE PATH
			new_content = open("/codis/files/" + base + "/" + arquivo[i], "r").read()
   			f.write(new_content)
   			f.close()


#---Joining 9 txts of each fold
for f in range(1,11):
	fold = f
	for i in range(1,11):
		if(i != fold):
			### UPDATE PATH
			with open("/codis/files/" + base + "/" + "fold" + str(fold) + "-junto.txt", "a") as f:
				### UPDATE PATH
				new_content = open("/codis/files/" + base + "/" + arquivo[i], "r").read()
	   			f.write(new_content)
	   			f.close()
