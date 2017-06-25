import os
import string

dicoLabels=dict()


import os
import sys
import string
annees=os.listdir("hasIpcCorr")
dicoClass=dict()
periodNumber=int(sys.argv[1])

from string import maketrans
tableTranslation=""
for p in string.punctuation:
	tableTranslation+=" "

trantab = maketrans(string.punctuation, tableTranslation)



dicoIdentifiant=dict()

cpt=0

limite=2001
limiteMin=limite + (periodNumber - 1)*2
limiteMax=limite+periodNumber*2

res=open("labels"+str(periodNumber))
idx=0
for chemin in res:
	dicoIdentifiant[idx]=chemin.strip()
	idx+=1
res.close()

res=open("../voc_freqmin100_docmax5000_classemax6")
voc=dict()
for ligne in res:
	mot=ligne.split("\t")[0].strip()
	voc[mot]=len(voc)
res.close()

matrix=[]

for idx in range(len(dicoIdentifiant)):
	fichier=dicoIdentifiant[idx]
	fichier=open(fichier)
	representation=[0]*len(voc)
	for ligne in fichier:
		if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("date :::") or ligne.startswith("description :::") or ligne.startswith("ipc :::"):
			continue
		else:	
			ligne=ligne.strip("abstract :::").strip("claim :::")
			ligne=ligne.translate(trantab)
			ligne=ligne.split(" ")
			for mot in ligne:
				mot=mot.strip().lower()
				if mot in voc:
					representation[voc[mot]]+=1
		
	matrix.append(representation)

res=open("matrix"+str(periodNumber), "w")
for ligne in matrix:
	for val in ligne:
		res.write(str(val)+"\t")
	res.write("\n")
res.close()



				
	
