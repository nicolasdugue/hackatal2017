import sys
import numpy as np

fichier=open("voc.tsv")
dico=dict()

borneMin=int(sys.argv[1])
borneMax=int(sys.argv[2])
nbClasseMax=int(sys.argv[3])
cpt=0

error=0
for ligne in fichier:
	try:
		tab=ligne.split("\t")
		mot=tab[0]
		freq=map(int, list(tab[1].strip("[").strip("]").replace(" ", "").split(",")))
		nbAnnee=int(tab[2])
		classes=tab[3]
		nbClasse=0
		for classe in ["A", "B", "C", "D", "E", "F", "G", "H"]:
			if classe in classes:
				nbClasse+=1
		docTotal=np.sum(np.array(freq))
		if not mot.isdigit() and nbAnnee > 1 and docTotal > borneMin and docTotal < borneMax and nbClasse < nbClasseMax:
			dico[tab[0].strip()]=ligne.strip()
			cpt+=1
	except IndexError:
		error+=1
		pass
print cpt
fichier =open("voc_freqmin"+str(borneMin)+"_freqmax"+str(borneMax), "w")
for mot in dico:
	fichier.write(dico[mot]+"\n")
fichier.close()
