import os
import string
annees=os.listdir("hasIpcCorr")
dicoFreq=dict()

dicoYear=dict()
#dicoClass

from string import maketrans


fichier=open("types.tsv")
vocabHapax=set()
for ligne in fichier:
	tab=ligne.split("\t")
	freq=int(tab[1].strip())
	if freq < 2:
		vocabHapax.add(tab[0].strip())

tableTranslation=""
for p in string.punctuation:
	tableTranslation+=" "

trantab = maketrans(string.punctuation, tableTranslation)

cptAnnee=0
for annee in annees:
	dicoDoc=dict()
	ensembleMotAnnee=set()
	fichiers=os.listdir("hasIpcCorr/"+annee)
	for f in fichiers:
		brevet=open("hasIpcCorr/"+annee+"/"+f)
		ensembleMotDoc=set()
		for ligne in brevet:
			if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("ipc :::") or ligne.startswith("date :::"):
				continue
			else:
				ligne=ligne.strip("abstract :::").strip("claim :::")
				ligne=ligne.translate(trantab)
				ligne=ligne.split(" ")
				for mot in ligne:
					mot=mot.strip().lower()
					if len(mot) > 3:
						if mot in vocabHapax:
							vocabHapax.remove(mot)
						else:
							if mot in ensembleMotAnnee:
								if mot not in ensembleMotDoc:
									ensembleMotDoc.add(mot)
									dicoDoc[mot]+=1
								
							else: #Pas vu cette annee
								ensembleMotAnnee.add(mot)
								if mot in dicoYear:
									dicoYear[mot]+=1
								else:
									dicoDoc[mot]=1
									ensembleMotDoc.add(mot)
									dicoYear[mot]=1
	for mot in dicoDoc:
		if mot not in dicoFreq:
			dicoFreq[mot]=[]
			for i in range(15):
				dicoFreq[mot].append(0)
		dicoFreq[mot][cptAnnee]+=dicoDoc[mot]								
	cptAnnee+=1
res=open("voc.tsv","w")
for mot in dicoDoc:
	if dicoDoc[mot] > 1:
		res.write(mot + "\t"+str(dicoFreq[mot])+"\t"+str(dicoDoc[mot])+"\t"+str(dicoYear[mot])+"\n")
res.close()
					

