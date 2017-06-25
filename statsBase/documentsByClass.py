import os
import string
annees=os.listdir("hasIpcCorr")
dicoClass=dict()


fichier=open("sortedDomainsUnique")
for ligne in fichier:
	dicoClass[ligne.strip()]=0

for annee in annees:
	fichiers=os.listdir("hasIpcCorr/"+annee)
	for f in fichiers:
		brevet=open("hasIpcCorr/"+annee+"/"+f)
		for ligne in brevet:
			if ligne.startswith("code :::") or ligne.startswith("file :::") or ligne.startswith("date :::") or ligne.startswith("description :::"):
				continue
			else:
				if ligne.startswith("ipc :::"):
					dicoClass[ligne.strip("ipc ::: ").split(" ")[0] ]+=1
	
res=open("NbDocByClass.tsv","w")
for classe in dicoClass:
	res.write(classe+"\t"+str(dicoClass[classe])+"\n")
res.close()
					

