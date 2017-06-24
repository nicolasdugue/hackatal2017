import os
import string
annees=os.listdir("hasIpcCorr")
dicoFreq=dict()
dicoDoc=dict()
#dicoClass

fichier=open("types.tsv")
vocabHapax=set()
for ligne in fichier:
	tab=ligne.split("\t")
	freq=int(tab[1].strip())
	if freq < 2:
		vocabHapax.add(tab[0].strip())

for annee in annees:
	fichiers=os.listdir("hasIpcCorr/"+annee)
	for f in fichiers:
		brevet=open("hasIpcCorr/"+annee+"/"+f)
		for ligne in brevet:
			ensembleMotDoc=set()
			if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("ipc :::") or ligne.startswith("date :::") or ligne.startswith("description :::"):
				continue
			else:
				ligne=ligne.strip("abstract :::").strip("claim :::")
				ligne=ligne.translate(None, string.punctuation)
				ligne=ligne.split(" ")
				for mot in ligne:
					mot=mot.strip().lower()
					if mot in vocabHapax:
						vocabHapax.remove(mot)
					else:
						if mot in ensembleMotDoc:
							dicoFreq[mot]+=1
						else:
							ensembleMotDoc.add(mot)
							if mot in dicoDoc:
								dicoDoc[mot]+=1
								dicoFreq[mot]+=1
							else:
								dicoDoc[mot]=1
								dicoFreq[mot]=1
res=open("voc.tsv","w")
for mot in dicoDoc:
	if dicoDoc[mot] > 1:
		res.write(mot + "\t"+str(dicoFreq[mot])+"\t"+str(dicoDoc[mot])+"\n")
res.close()
					

