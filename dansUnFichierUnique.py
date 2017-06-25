import os
import string
import numpy as np
annees=os.listdir("hasIpcCorr")
dicoFreq=dict()

dicoYear=dict()
dicoClass=dict()

from string import maketrans


fichier=open("types.tsv")
vocabHapax=set()
for ligne in fichier:
	tab=ligne.split("\t")
	freq=int(tab[1].strip())
	if freq < 2:
		vocabHapax.add(tab[0].strip().lower())

tableTranslation=""
for p in string.punctuation:
	tableTranslation+=" "

trantab = maketrans(string.punctuation, tableTranslation)

cptAnnee=0
annees.sort()
for annee in annees:
	dicoDoc=dict()
	fichiers=os.listdir("hasIpcCorr/"+annee)
	for f in fichiers:
		brevet=open("hasIpcCorr/"+annee+"/"+f)
		ensembleMotDoc=set()
		ensembleClass=set()
		for ligne in brevet:
			if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("date :::") or ligne.startswith("description :::"):
				continue
			else:
				if ligne.startswith("ipc :::"):
					ensembleClass.add(ligne.strip("ipc ::: ")[0])
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
								for classe in ensembleClass:
									if (mot,classe) in dicoClass:
										dicoClass[(mot,classe)]+=1
									else:
										dicoClass[(mot,classe)]=1
								if mot in dicoDoc:
									if mot not in ensembleMotDoc:
										ensembleMotDoc.add(mot)
										dicoDoc[mot]+=1
								else: #Pas vu cette annee
									dicoDoc[mot]=1
									if mot in dicoYear:
										dicoYear[mot]+=1
									else:
										ensembleMotDoc.add(mot)
										dicoYear[mot]=1
	for mot in dicoDoc:
		if mot not in dicoFreq:
			dicoFreq[mot]=[]
			for i in range(15):
				dicoFreq[mot].append(0)
		dicoFreq[mot][cptAnnee]=dicoDoc[mot]								
	cptAnnee+=1
res=open("voc.tsv","w")
for mot in dicoFreq:
	if not mot.isdigit():
		if dicoYear[mot] > 1:
			s=[]
			for classe in ["A", "B", "C", "D", "E", "F", "G", "H"]:
				if (mot, classe) in dicoClass:
					s.append(dicoClass[(mot, classe)])	
				else:
					s.append(0)
			somme=np.sum(s)
			if somme == 0:
				s2=s
			else:
				s2=map(lambda x: x / float(somme), s)
			res.write(mot + "\t"+str(dicoFreq[mot])+"\t"+str(dicoYear[mot])+"\t"+str(s)+"\t"+str(s2)+"\n")
res.close()
					

